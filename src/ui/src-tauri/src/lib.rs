// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
async fn generate_ppt(design_path: String, input_path: String, input_text: String, out_path: String, is_raw: bool, ai_provider: String, api_key: String, language: String) -> Result<(), String> {
    use std::process::Command;
    use std::io::Write;
    
    let actual_input_path = if !input_text.is_empty() {
        let temp_path = std::env::temp_dir().join("ppt_input.txt");
        let mut file = std::fs::File::create(&temp_path).map_err(|e| e.to_string())?;
        file.write_all(input_text.as_bytes()).map_err(|e| e.to_string())?;
        temp_path.to_string_lossy().to_string()
    } else {
        input_path
    };

    let mut cmd = Command::new("python");
    cmd.arg("../../engine/design2ppt.py")
       .arg("--design").arg(design_path)
       .arg("--input").arg(actual_input_path)
       .arg("--out").arg(out_path);
       
    if is_raw {
        cmd.arg("--raw");
        cmd.arg("--provider").arg(ai_provider);
        cmd.arg("--api-key").arg(api_key);
        cmd.arg("--language").arg(language);
    }

    let status = cmd.status()
        .map_err(|e| format!("Failed to spawn python process: {}", e))?;

    if status.success() {
        Ok(())
    } else {
        Err(format!("design2ppt exited with {}", status))
    }
}

#[tauri::command]
async fn chat_with_ai(message: String, provider: String, api_key: String, language: String) -> Result<String, String> {
    use std::process::Command;
    let output = Command::new("python")
        .arg("../../engine/chat.py")
        .arg("--message").arg(message)
        .arg("--provider").arg(provider)
        .arg("--api-key").arg(api_key)
        .arg("--language").arg(language)
        .output()
        .map_err(|e| format!("Failed to spawn python process: {}", e))?;

    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();

    if output.status.success() {
        Ok(stdout)
    } else {
        Err(format!("Error: {}", stderr))
    }
}

#[tauri::command]
async fn get_theme_tokens(design_path: String) -> Result<String, String> {
    use std::process::Command;
    let output = Command::new("python")
        .arg("../../engine/design2ppt.py")
        .arg("--design").arg(design_path)
        .arg("--parse-only")
        .arg("--out").arg("dummy")
        .output()
        .map_err(|e| format!("Failed to spawn python process: {}", e))?;

    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();

    if output.status.success() {
        Ok(stdout)
    } else {
        Err(format!("Error: {}", stderr))
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![generate_ppt, chat_with_ai, get_theme_tokens])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

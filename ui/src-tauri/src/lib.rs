// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
async fn generate_ppt(design_path: String, input_path: String, out_path: String, is_raw: bool) -> Result<(), String> {
    use std::process::Command;
    
    // Determine the path to the engine directory relative to current execution context.
    // For MVP, assuming it's executed where engine/ is parallel to ui/
    let mut cmd = Command::new("python");
    cmd.arg("../engine/design2ppt.py")
       .arg("--design").arg(design_path)
       .arg("--input").arg(input_path)
       .arg("--out").arg(out_path);
       
    if is_raw {
        cmd.arg("--raw");
    }

    let status = cmd.status()
        .map_err(|e| format!("Failed to spawn python process: {}", e))?;

    if status.success() {
        Ok(())
    } else {
        Err(format!("design2ppt exited with {}", status))
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![generate_ppt])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#!/usr/bin/env python3
"""
Ace Combat 2 Recompiled — Detector y Preparador Universal de Disco
Soporte completo: PAL (España/Europa SCES-00710), NTSC-U (USA SLUS-00404 v1.0/v1.1), NTSC-J (Japón SLPS-00830 / The Best SLPS-91060 / NamCollection SLPM-80512)
Formatos: .PBP, .BIN/.CUE, .ISO, .IMG, .CHD
"""

import os
import sys
import struct
import zlib
import re
import shutil
from pathlib import Path

KNOWN_VERSIONS = {
    "SCES_006.99": {
        "serial": "SCES-00699",
        "title": "Ace Combat 2 (Europe - PAL)",
        "region": "PAL",
        "hz": 50.0,
        "lang": "en",
        "boot_exe": "SCES_006.99"
    },
    "SCES_007.10": {
        "serial": "SCES-00710",
        "title": "Ace Combat 2 (Europe / España - PAL)",
        "region": "PAL",
        "hz": 50.0,
        "lang": "es",
        "boot_exe": "SCES_007.10"
    },
    "SLUS_004.04": {
        "serial": "SLUS-00404",
        "title": "Ace Combat 2 (USA - NTSC-U)",
        "region": "NTSC-U",
        "hz": 59.94,
        "lang": "en",
        "boot_exe": "SLUS_004.04"
    },
    "SLPS_008.30": {
        "serial": "SLPS-00830",
        "title": "Ace Combat 2 (Japan - NTSC-J v1.0)",
        "region": "NTSC-J",
        "hz": 59.94,
        "lang": "ja",
        "boot_exe": "SLPS_008.30"
    },
    "SLPS_910.60": {
        "serial": "SLPS-91060",
        "title": "Ace Combat 2 (Japan - PlayStation The Best)",
        "region": "NTSC-J",
        "hz": 59.94,
        "lang": "ja",
        "boot_exe": "SLPS_910.60"
    },
    "SLPM_805.12": {
        "serial": "SLPM-80512",
        "title": "Ace Combat 2 (Japan - NamCollection)",
        "region": "NTSC-J",
        "hz": 59.94,
        "lang": "ja",
        "boot_exe": "SLPM_805.12"
    }
}

def extract_pbp(pbp_path: Path, out_bin: Path):
    print(f"[*] Desempaquetando imagen Sony PSP/PS3 PBP: {pbp_path.name}...")
    with open(pbp_path, "rb") as f:
        header = f.read(40)
        if header[:4] != b"\x00PBP":
            print("[!] Error: No es un archivo PBP valido.")
            return False
            
        offsets = struct.unpack("<8I", header[8:40])
        psar_offset = offsets[7]
        f.seek(psar_offset)
        psar_magic = f.read(12)
        if psar_magic[:4] != b"PSAR":
            print("[!] Error: Magic PSAR invalido.")
            return False
            
        f.seek(psar_offset + 0x200)
        header_data = f.read(0x4000)
        
        psiso_idx = header_data.find(b"PSISOIMG0000")
        if psiso_idx == -1:
            f.seek(psar_offset)
            full_search = f.read(0x100000)
            psiso_idx = full_search.find(b"PSISOIMG0000")
            table_offset = psar_offset + psiso_idx + 0x400 if psiso_idx != -1 else psar_offset + 0x4000
        else:
            table_offset = psar_offset + 0x200 + psiso_idx + 0x400

        f.seek(table_offset)
        table_raw = f.read(0x100000)
        
        entries = []
        for i in range(0, len(table_raw), 32):
            if i + 32 > len(table_raw):
                break
            chunk = table_raw[i:i+32]
            off, length = struct.unpack("<II", chunk[:8])
            if off == 0 and length == 0:
                break
            entries.append((off, length))

        if not entries:
            f.seek(psar_offset + 0x400)
            table_raw = f.read(0x100000)
            for i in range(0, len(table_raw), 8):
                chunk = table_raw[i:i+8]
                off, length = struct.unpack("<II", chunk)
                if off == 0 and length == 0:
                    break
                entries.append((off, length))

        print(f"    Total bloques encontrados: {len(entries)}")
        with open(out_bin, "wb") as out_f:
            for i, (off, length) in enumerate(entries):
                if length == 0:
                    continue
                f.seek(psar_offset + off)
                comp_data = f.read(length)
                try:
                    decomp = zlib.decompress(comp_data)
                    out_f.write(decomp)
                except Exception:
                    out_f.write(comp_data)
                    
                if i > 0 and i % 2500 == 0:
                    print(f"    ... procesados {i} bloques de sectores...")
                    
    print(f"[+] Extraccion PBP completada: {out_bin.name} ({out_bin.stat().st_size // (1024*1024)} MB)")
    return True

def detect_serial(bin_path: Path):
    with open(bin_path, "rb") as f:
        data = f.read(4 * 1024 * 1024)
        m = re.search(rb'(SLES|SLUS|SCES|SCPS|SLED|SLPS|SCED|SCUS|SLPM)[_-](\d{3})\.?(\d{2})', data, re.IGNORECASE)
        if m:
            prefix = m.group(1).decode('ascii').upper()
            num1 = m.group(2).decode('ascii')
            num2 = m.group(3).decode('ascii')
            key = f"{prefix}_{num1}.{num2}"
            serial = f"{prefix}-{num1}{num2}"
            return key, serial
    return None, None

def write_cue(cue_path: Path, bin_name: str):
    cue_content = f'FILE "{bin_name}" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n'
    with open(cue_path, "w", encoding="utf-8") as f:
        f.write(cue_content)
    print(f"[+] Generado descriptor CUE: {cue_path.name}")

def update_configs(project_root: Path, cue_path: Path, serial: str, version_info: dict):
    cue_forward = str(cue_path.resolve()).replace("\\", "/")
    region = version_info.get("region", "NTSC-U")
    hz = version_info.get("hz", 59.94)
    boot_exe = version_info.get("boot_exe", f"{serial.replace('-', '_')[:4]}_{serial.replace('-', '_')[5:8]}.{serial.replace('-', '_')[8:]}")
    
    # 1. Update settings.toml
    for sfile in [project_root / "settings.toml", project_root / "build-release" / "settings.toml"]:
        if sfile.exists():
            text = sfile.read_text(encoding="utf-8", errors="replace")
            text = re.sub(r'path\s*=\s*"[^"]*"', f'path = "{cue_forward}"', text)
            if "region" in text:
                text = re.sub(r'region\s*=\s*"[^"]*"', f'region = "{region.lower()}"', text)
            sfile.write_text(text, encoding="utf-8")
            print(f"[+] Actualizado {sfile.name} -> {cue_forward}")

    # 2. Update game.toml
    for gtoml in [project_root / "game.toml", project_root / "build-release" / "game.toml"]:
        if gtoml.exists():
            text = gtoml.read_text(encoding="utf-8", errors="replace")
            text = re.sub(r'id\s*=\s*"[^"]*"', f'id = "{serial}"', text)
            text = re.sub(r'disc\s*=\s*"[^"]*"', f'disc = "{cue_forward}"', text)
            text = re.sub(r'exe\s*=\s*"[^"]*"', f'exe = "disc/{boot_exe}"', text)
            gtoml.write_text(text, encoding="utf-8")
            print(f"[+] Actualizado {gtoml.name} -> {serial} (Region: {region}, {hz} Hz)")

def main():
    print("=" * 65)
    print("  Ace Combat 2 Recompiled — Detector y Preparador Universal")
    print("  Soporte Completo: PAL (Europa/España), NTSC-U (USA), NTSC-J (Japón)")
    print("=" * 65)

    base_dir = Path(__file__).resolve().parent.parent
    disc_dir = base_dir / "disc"
    disc_dir.mkdir(parents=True, exist_ok=True)
    
    target_file = None
    if len(sys.argv) > 1:
        cand = Path(sys.argv[1])
        if cand.is_file():
            target_file = cand

    if not target_file:
        extensions = [".pbp", ".cue", ".bin", ".iso", ".img", ".chd"]
        search_dirs = [disc_dir, base_dir]
        
        candidates = []
        for sdir in search_dirs:
            if sdir.exists():
                for ext in extensions:
                    candidates.extend(list(sdir.glob(f"*{ext}")))
                    candidates.extend(list(sdir.glob(f"*{ext.upper()}")))

        clean_cands = []
        for c in candidates:
            if c.name.lower() in ["acecombat2.cue", "acecombat2.bin"] and c.parent == disc_dir:
                clean_cands.insert(0, c)
            else:
                clean_cands.append(c)
                
        if clean_cands:
            target_file = clean_cands[0]

    if not target_file:
        print("\n[!] No se encontro ninguna imagen de disco en la carpeta.")
        print("    Por favor, coloca tu copia de Ace Combat 2 (.PBP, .ISO, .BIN, .CUE, .CHD)")
        print(f"    en: {disc_dir} o en la raiz del proyecto y vuelve a ejecutar este script.")
        input("\nPulsa Enter para salir...")
        sys.exit(1)

    print(f"\n[*] Archivo detectado: {target_file}")
    
    bin_file = disc_dir / "AceCombat2.bin"
    cue_file = disc_dir / "AceCombat2.cue"

    suf = target_file.suffix.lower()
    if suf == ".pbp":
        ok = extract_pbp(target_file, bin_file)
        if not ok:
            sys.exit(1)
        write_cue(cue_file, "AceCombat2.bin")
    elif suf == ".cue":
        cue_file = target_file
        with open(target_file, "r", encoding="utf-8", errors="replace") as f:
            m = re.search(r'FILE\s+"([^"]+)"', f.read(), re.I)
            if m:
                bin_file = target_file.parent / m.group(1)
            else:
                bin_file = target_file.with_suffix(".bin")
    elif suf in [".bin", ".iso", ".img"]:
        if target_file.resolve() != bin_file.resolve():
            print(f"[*] Vinculando {target_file.name} -> {bin_file}...")
            try:
                shutil.copy2(target_file, bin_file)
            except Exception:
                bin_file = target_file
        write_cue(cue_file, bin_file.name)

    boot_key, detected_serial = detect_serial(bin_file) if bin_file.exists() else (None, None)
    is_pal = detected_serial and (detected_serial.startswith("SCES") or detected_serial.startswith("SLES"))
    version_info = KNOWN_VERSIONS.get(boot_key, {
        "serial": detected_serial or ("SCES-00710" if is_pal else "SLUS-00404"),
        "title": f"Ace Combat 2 ({detected_serial or 'Desconocida'})",
        "region": "PAL" if is_pal else "NTSC-U",
        "hz": 50.0 if is_pal else 59.94,
        "lang": "es" if is_pal else "en",
        "boot_exe": boot_key or ("SCES_007.10" if is_pal else "SLUS_004.04")
    })

    print("-" * 65)
    print(f"  Version identificada: {version_info['title']}")
    print(f"  Serial PS1:           {version_info['serial']}")
    print(f"  Region de video:      {version_info['region']} ({version_info['hz']} Hz)")
    print("-" * 65)

    update_configs(base_dir, cue_file, version_info["serial"], version_info)
    print("\n[OK] Configuracion completada con exito.")
    print("    El juego esta listo para iniciarse con JUGAR_ACE_COMBAT_2.bat.")

if __name__ == "__main__":
    main()

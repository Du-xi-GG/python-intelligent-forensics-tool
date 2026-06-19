import os
import hashlib
import math
import time
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet


# HASH

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except:
        return "ERROR"


# ENTROPY

def calculate_entropy(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = data.count(bytes([x])) / len(data)
            if p_x > 0:
                entropy -= p_x * math.log2(p_x)
        return round(entropy, 3)
    except:
        return 0


# FEATURE EXTRACTION

def scan_directory(directory):
    records = []

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                stat = os.stat(path)
                records.append({
                    "file_name": file,
                    "path": path,
                    "extension": os.path.splitext(file)[1],
                    "size": stat.st_size,
                    "modified_time": stat.st_mtime,
                    "entropy": calculate_entropy(path),
                    "sha256": calculate_sha256(path)
                })
            except:
                continue

    return pd.DataFrame(records)


# MACHINE LEARNING

def run_ml(df):
    df_ml = df.copy()
    df_ml["ext_code"] = df_ml["extension"].astype("category").cat.codes

    features = df_ml[["size", "entropy", "ext_code", "modified_time"]]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42
    )

    df["ml_label"] = model.fit_predict(features)
    df["status"] = df["ml_label"].apply(
        lambda x: "Sumnjiv (ML)" if x == -1 else "Normalan"
    )

    return df


# DISPLAY FUNCTIONS

def show_files_with_hash(df):
    print("\nFAJLOVI + SHA-256\n")
    for _, row in df.iterrows():
        print(f"{row['file_name']} | {row['sha256']}")

def show_entropy(df):
    print("\nENTROPIJA FAJLOVA\n")
    for _, row in df.iterrows():
        flag = " <-- VISOKA ENTROPIJA" if row["entropy"] > 7 else ""
        print(f"{row['file_name']} | Entropija: {row['entropy']}{flag}")

def show_suspicious(df):
    suspicious = df[df["status"].str.contains("Sumnjiv")]
    if suspicious.empty:
        print("\nNema sumnjivih fajlova.")
    else:
        print("\nSUMNJIVI FAJLOVI (ML)\n")
        print(suspicious[["file_name", "entropy", "size", "status"]])


# REPORTS

def generate_csv(df):
    name = f"forenzicki_izvestaj_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(name, index=False)
    print(f"[✔] CSV izveštaj: {name}")

def generate_pdf(df):
    name = f"forenzicki_izvestaj_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(name)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Forenzicki izvestaj - Analiza fajlova", styles["Title"]))

    table_data = [["Fajl", "Entropija", "Velicina", "Status"]]
    for _, row in df.iterrows():
        table_data.append([
            row["file_name"],
            row["entropy"],
            row["size"],
            row["status"]
        ])

    elements.append(Table(table_data))
    doc.build(elements)

    print(f"[✔] PDF izveštaj: {name}")


# MENU

def menu():
    print("""
=== INTELIGENTNI FORENZIČKI ALAT ===
1 - Prikaži sve fajlove + hash
2 - Prikaži entropiju fajlova
3 - Prikaži sumnjive fajlove (ML)
4 - Generiši CSV izveštaj
5 - Generiši PDF izveštaj
0 - Izlaz
""")


# MAIN

def main():
    directory = input("Unesite putanju direktorijuma za skeniranje: ")
    df = scan_directory(directory)
    df = run_ml(df)

    while True:
        menu()
        choice = input("Izaberite opciju: ")

        if choice == "1":
            show_files_with_hash(df)
        elif choice == "2":
            show_entropy(df)
        elif choice == "3":
            show_suspicious(df)
        elif choice == "4":
            generate_csv(df)
        elif choice == "5":
            generate_pdf(df)
        elif choice == "0":
            print("Izlaz iz programa.")
            break
        else:
            print("Nepoznata opcija.")

if __name__ == "__main__":
    main()

"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import os
import glob
import pandas as pd

def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months

    """
    input_dir = "files/input/"
    output_dir = "files/output/"
    
    os.makedirs(output_dir, exist_ok=True)
    
    all_files = glob.glob(os.path.join(input_dir, "*.csv.zip"))
    if not all_files:
        return

    df_list = [pd.read_csv(file) for file in all_files]
    df = pd.concat(df_list, ignore_index=True)
    df.columns = df.columns.str.strip()

    mortgage_col = "mortgage" if "mortgage" in df.columns else "mortage"
    
    df_client = df[["client_id", "age", "job", "marital", "education", "credit_default", mortgage_col]].copy()
    df_client.columns = ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]
    
    df_client["job"] = df_client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    df_client["education"] = df_client["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    df_client["credit_default"] = df_client["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    df_client["mortgage"] = df_client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
    
    df_client.to_csv(os.path.join(output_dir, "client.csv"), index=False)

    month_mapping = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    
    prev_camp_col = "previous_campaign_contacts" if "previous_campaign_contacts" in df.columns else "previous_campaing_contacts"
    
    df_campaign = df[[
        "client_id", "number_contacts", "contact_duration", 
        prev_camp_col, "previous_outcome", "campaign_outcome", "day", "month"
    ]].copy()
    
    df_campaign.columns = [
        "client_id", "number_contacts", "contact_duration", 
        "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "day", "month"
    ]
    
    df_campaign["previous_outcome"] = df_campaign["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    df_campaign["campaign_outcome"] = df_campaign["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    
    day_str = df_campaign["day"].astype(str).str.zfill(2)
    month_str = df_campaign["month"].str.lower().map(month_mapping)
    
    df_campaign["last_contact_date"] = "2022-" + month_str + "-" + day_str
    
    df_campaign = df_campaign.drop(columns=["day", "month"])
    df_campaign.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)

    cons_price_col = "cons_price_idx" if "cons_price_idx" in df.columns else "const_price_idx"
    euribor_col = "euribor_three_months" if "euribor_three_months" in df.columns else "eurobor_three_months"
    
    df_economics = df[["client_id", cons_price_col, euribor_col]].copy()
    df_economics.columns = ["client_id", "cons_price_idx", "euribor_three_months"]
    
    df_economics.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

if __name__ == "__main__":
    clean_campaign_data()

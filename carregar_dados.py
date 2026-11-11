import numpy as np
import pandas as pd
from pathlib import Path

numero_eduardo = 54397
numero_felipe = 54698

ficheiro_bruto = Path("data/raw/household_power_consumption.txt")

soma_numeros_alunos = numero_eduardo + numero_felipe

rng = np.random.default_rng(soma_numeros_alunos)
inicio = pd.Timestamp(rng.choice(pd.date_range("2007-01-01", "2009-05-01", freq="MS")))
fim = inicio + pd.DateOffset(months=18)   
print(f"Janela do grupo: {inicio:%Y-%m-%d} → {fim:%Y-%m-%d} (18 meses)  | seed = {soma_numeros_alunos}")

DTYPES = {
    "Global_active_power": "float32",
    "Global_reactive_power": "float32",
    "Voltage": "float32",
    "Global_intensity": "float32",
    "Sub_metering_1": "float32",
    "Sub_metering_2": "float32",
    "Sub_metering_3": "float32",
}

def carregar_dados(caminho=ficheiro_bruto, inicio=None, fim=None):

    df = pd.read_csv(caminho, sep=';', na_values="?",
                     low_memory=False)

    dt = pd.to_datetime(df.pop("Date") + " " + df.pop("Time"), format="%d/%m/%Y %H:%M:%S")
    df.index = pd.DatetimeIndex(dt, name="Datetime")
    df = df.sort_index()

    if inicio is not None and fim is not None:
        df = df.loc[(df.index >= inicio) & (df.index < fim)]

    validar(df)
    
    return df

def validar(df):

    assert isinstance(df.index, pd.DatetimeIndex)
    assert df.index.is_unique
    assert df.index.is_monotonic_increasing
    assert df["Voltage"].dropna().between(150, 300).all()
    assert (df["Global_intensity"].dropna() >= 0).all()
    
df = carregar_dados(inicio=inicio, fim=fim)
print(df.head())
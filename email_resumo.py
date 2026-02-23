import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import date
import os

CSV_URL = "https://github.com/brunoviniciusramosps-ctrl/automation-tracker/main/demandas.csv"

def gerar_resumo(df):
    total = len(df)
    atrasadas = len(df[df["SLA Status"] == "🔴 Atrasado"])
    criticas = len(df[df["Prioridade"] == "Crítica"])
    concluidas = len(df[df["Status"] == "Concluído"])

    return f"""
Resumo Executivo - Automation Tracker
Data: {date.today().strftime('%d/%m/%Y')}

Total de demandas: {total}
Demandas atrasadas: {atrasadas}
Demandas críticas: {criticas}
Demandas concluídas: {concluidas}

Dashboard online:
https://dashaccountbamaq.streamlit.app/
"""


def enviar_email(resumo):
    msg = EmailMessage()
    msg["Subject"] = "📊 Resumo Executivo - Automação"
    msg["From"] = os.environ["EMAIL_REMETENTE"]
    msg["To"] = os.environ["EMAIL_DESTINO"]
    msg.set_content(resumo)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.environ["EMAIL_REMETENTE"],
            os.environ["EMAIL_SENHA"]
        )
        smtp.send_message(msg)


def main():
    df = pd.read_csv(CSV_URL)
    resumo = gerar_resumo(df)
    enviar_email(resumo)


if __name__ == "__main__":
    main()

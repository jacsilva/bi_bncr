"""Configuração e abertura da conexão JDBC (Teiid) com o Sinesp PPe."""

import os
import shutil
from pathlib import Path

from dotenv import load_dotenv

# Diretórios do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

load_dotenv(BASE_DIR / ".env")

# Credenciais e endpoint
LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")
URL = os.getenv("URL")

# Artefatos de configuração
JDBC_JAR = CONFIG_DIR / "jboss-dv-6.3.0-teiid-jdbc.jar"
KEYSTORE_PATH = CONFIG_DIR / "daas.serpro.gov.br.jks"
KEYSTORE_TYPE = "JKS"
JDBC_DRIVER = "org.teiid.jdbc.TeiidDriver"


def _start_jvm():
    """Inicia a JVM (se necessário) e configura o trust store SSL."""
    import jpype

    if not shutil.which("java"):
        raise RuntimeError(
            "Java não está instalado. JayDeBeApi requer Java para funcionar.\n"
            "Instale o JDK: sudo apt install default-jdk"
        )

    if not jpype.isJVMStarted():
        jpype.startJVM(
            jpype.getDefaultJVMPath(),
            f"-Djava.class.path={JDBC_JAR}",
            convertStrings=False,
        )

        System = jpype.JClass("java.lang.System")
        System.setProperty("javax.net.ssl.trustStore", str(KEYSTORE_PATH))
        System.setProperty("javax.net.ssl.trustStoreType", KEYSTORE_TYPE)

        # Silencia os avisos de log do driver Teiid (ex.: cipher suite anônimo).
        # O handler de console do root logger só deixa passar erros (SEVERE);
        # atuar no handler é estável (o root logger não é coletado pelo GC).
        Logger = jpype.JClass("java.util.logging.Logger")
        Level = jpype.JClass("java.util.logging.Level")
        root = Logger.getLogger("")
        for handler in root.getHandlers():
            handler.setLevel(Level.SEVERE)


def get_connection():
    """Abre e retorna uma conexão JDBC com o banco Teiid."""
    import jaydebeapi

    _start_jvm()

    print("\nTentando conectar ao banco via JDBC (JayDeBeApi)...")

    conn = jaydebeapi.connect(
        JDBC_DRIVER,
        URL,
        {"user": LOGIN, "password": SENHA},
    )

    print("Conexão estabelecida com sucesso!")
    return conn

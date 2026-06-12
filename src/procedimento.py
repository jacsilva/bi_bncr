"""Execução das queries SQL e conversão/serialização dos resultados."""

import json
import warnings

# JayDeBeApi avisa sobre tipos JDBC sem mapeamento (ex.: JAVA_OBJECT);
# tratamos esses campos manualmente, então o aviso é irrelevante.
warnings.filterwarnings("ignore", message="No type mapping for JDBC type")

# Prefixo das colunas RAW/binárias (GUIDs de delegacia), convertidas p/ hex.
# Cobre ID_UN_DELEGACIA_REGISTRO/_AFETO/_ORIGEM_ENC/_DESTINO_ENC etc.
BINARY_FIELD_PREFIXES = ("ID_UN_DELEGACIA",)


def is_binary_field(col):
    """Indica se a coluna é um campo binário (deve virar hexadecimal)."""
    return col.startswith(BINARY_FIELD_PREFIXES)


def _strip_nul(text):
    """Remove bytes nulos: Postgres não aceita \\u0000 em text/JSONB."""
    return text.replace("\x00", "") if "\x00" in text else text


def to_python(obj):
    """Converte um valor retornado pelo JDBC para um tipo Python serializável."""
    if obj is None:
        return None
    if isinstance(obj, (int, float, bool)):
        return obj
    if isinstance(obj, str):
        return _strip_nul(obj)
    return _strip_nul(str(obj))


def convert_bytes_field(value):
    """Converte um campo binário para sua representação hexadecimal."""
    if value is None:
        return None
    if isinstance(value, str):
        return _strip_nul(value)
    try:
        return "".join(format(b, "02x") for b in bytes(value))
    except Exception:
        return _strip_nul(str(value))


def _split_queries(sql_content):
    """Divide o conteúdo SQL em queries individuais."""
    return [q.strip() for q in sql_content.split(";") if q.strip()]


def run_queries(conn, sql_content):
    """Executa todas as queries do conteúdo SQL e retorna os resultados."""
    queries = _split_queries(sql_content)
    print(f"Encontradas {len(queries)} queries para executar")

    cursor = conn.cursor()
    results = []

    try:
        for i, query in enumerate(queries):
            print(f"\nExecutando query {i + 1}/{len(queries)}...")
            try:
                cursor.execute(query)
                columns = (
                    [to_python(desc[0]) for desc in cursor.description]
                    if cursor.description
                    else []
                )
                rows = cursor.fetchall()

                data_rows = []
                for row in rows:
                    row_dict = {}
                    for col, val in zip(columns, row):
                        if is_binary_field(col):
                            row_dict[col] = convert_bytes_field(val)
                        else:
                            row_dict[col] = to_python(val)
                    data_rows.append(row_dict)

                results.append(
                    {
                        "query_index": i + 1,
                        "columns": columns,
                        "row_count": len(rows),
                        "data": data_rows,
                    }
                )
                print(f"  -> {len(rows)} linhas retornadas")
            except Exception as e:
                print(f"  -> Erro: {e}")
                results.append({"query_index": i + 1, "error": str(e)})
    finally:
        cursor.close()

    return results


def save_results(results, output_file):
    """Salva os resultados em um arquivo JSON."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\nTotal: {len(results)} queries processadas, salvos em {output_file}")

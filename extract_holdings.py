from argparse import ArgumentParser
from csv import DictReader

from rows.utils import CsvLazyDictWriter, open_compressed
from tqdm import tqdm


def convert_row(row):
    return {
        "holding_cnpj": row["cnpj_cpf_do_socio"],
        "holding_razao_social": row["nome_socio"],
        "cnpj": row["cnpj"],
    }


def filter_csv(input_filename, output_filename, filter_function, convert_function, progress=True):
    fobj_reader = open_compressed(input_filename, mode="r")
    fobj_writer = open_compressed(output_filename, mode="w")
    csv_reader = DictReader(fobj_reader)
    csv_writer = CsvLazyDictWriter(fobj_writer)
    if progress:
        csv_reader = tqdm(csv_reader)
    for row in csv_reader:
        if filter_function(row):
            csv_writer.writerow(convert_function(row))
    fobj_reader.close()
    fobj_writer.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    filter_csv(
        args.input_filename,
        args.output_filename,
        lambda row: row["identificador_de_socio"] == "1",
        convert_function=convert_row,
        progress=True,
    )

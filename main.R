library(here, quietly = T)

source(here("dependencias",
            "r_functions.R"))$value


args = commandArgs(trailingOnly = TRUE)
n_trat = as.numeric(args[1])
index = as.numeric(args[2:(n_trat + 1)])
file = args[n_trat + 2]
mode = args[n_trat + 3]


# Esse loop vai pegar o resultado de cada simulação
# e realizar operações específicas de acordo com o
# arquivo (file) em questão.
for(i in 1:(length(index))){

  # Read the Output file

  number_rows = nrow_fun(index, i, file)

  x = read.table(paste0("C:/DSSAT47/", mode, "/", file),
                 skip = index[i] - 1,
                 sep = "",
                 nrows = number_rows,
                 header = T,
                 na.strings = "",
                 fill = T,
                 comment.char = "")

  name = read.table(paste0("C:/DSSAT47/", mode, "/", file),

                    skip = (index[i] - identify_out(file)) + 5,
                    nrows = 1)

  name = as.character(name[["V5"]])


  if((stringr::str_remove(file,".OUT")) == "PlantGro"){

    # Armengue para arrumar a coluna de Yield:
    if(number_rows >= 0){
      x = dplyr::mutate(x, HWAD = readr::read_fwf(paste0("C:/DSSAT47/", mode, "/", file),
                                                skip = index[i],
                                                n_max = nrow_fun(index, i, file),
                                                col_positions = readr::fwf_cols("HWAD" = c(112, 117)))[[1]])
    }
    else{
      x = dplyr::mutate(x, HWAD = readr::read_fwf(paste0("C:/DSSAT47/", mode, "/", file),
                                                skip = index[i],
                                                n_max = nrow(x),
                                                col_positions = readr::fwf_cols("HWAD" = c(112, 117)))[[1]])
    }


    # Dado que esse é o primeiro arquivo .OUT a ser processado por esse
    # script (defini isso em ''main.py''), o presente loop vai ser
    # responsável por criar:

    # 1) Diretório de outputs de cada simulação;
    # 2) auxiliar.csv;
    # 3) SimResults.csv dentro do diretório de cada simulação

    # Pegar DAS_inicial
    DAS_inicial = dplyr::first(x$DAS)

    # Pegar data de plantio
    x = dplyr::mutate(x, date = fazer_data(DOY, X.YEAR))

    plantio = data_plantio(x)

    # Identificar mês da Data de Plantio
    mes_plantio = as.character(lubridate::month(plantio,
                                   label = T))

    # Identificar dia do Mês em que ocorre o Plantio
    dia_mes = lubridate::mday(plantio)

    # Mês e dia em que ocorre a colheita
    colheita = data_colheita(x)
    mes_colheita = as.character(lubridate::month(colheita, label = T))
    dia_colheita = lubridate::mday(colheita)

    # 1) Criar diretório
    nome_pasta = paste0(name, "_", dia_mes, "_", mes_plantio, "_", dia_colheita, "_", mes_colheita)

    dir.create(here("Outputs", nome_pasta))

    # 2) Auxiliary file
    information = data.frame("simulation_n" = i,
                             "name" = name,
                             "DAS" = DAS_inicial,
                             "mes_plantio" = mes_plantio,
                             "dia_mes" = dia_mes,
                             "data_plantio" = plantio,
                             "mes_colheita" = mes_colheita,
                             "dia_mes_colheita" = dia_colheita,
                             "data_colheita" = colheita,
                             "Final Yield" = dplyr::last(x$HWAD))

    if(file.exists(here("Outputs",
                        "auxiliar.csv"))){
      # Se existir = Append
      write.table(information,
                  here("Outputs", "auxiliar.csv"),
                  row.names = F,
                  append = T,
                  col.names = F,
                  sep = ",")
    }
    else{
      # Não existindo = Create
      write.table(information,
                  here("Outputs", "auxiliar.csv"),
                  row.names = F,
                  sep = ",")
    }


    # 3) Criar SimResults.csv

    # Correção da correspondência entre DAS x DAP
    x = dplyr::mutate(x, DAS = DAS + 1)

    # Salvar SimResults.csv
    write.csv(x, here("Outputs", nome_pasta,
                      "SimResults.csv"), row.names = F)

  }

  else if((stringr::str_remove(file,".OUT")) == "Weather"){

    # Pegar informações do diretório de Outputs
    information = read.csv(here("Outputs",
                                "auxiliar.csv"))

    mes_plantio = information[[i, "mes_plantio"]]
    dia_mes = information[[i, "dia_mes"]]
    mes_colheita = information[[i, "mes_colheita"]]
    dia_colheita = information[[i, "dia_mes_colheita"]]

    nome_pasta = paste0(name, "_", dia_mes, "_", mes_plantio, "_", dia_colheita, "_", mes_colheita)
    # Salvar
    join_with_existing(x, nome_pasta, file)
  }

  else if((stringr::str_remove(file,".OUT")) == "PlantGrf"){

    # Pegar informações do diretório de Outputs
    information = read.csv(here("Outputs",
                                "auxiliar.csv"))

    mes_plantio = information[[i, "mes_plantio"]]
    dia_mes = information[[i, "dia_mes"]]
    mes_colheita = information[[i, "mes_colheita"]]
    dia_colheita = information[[i, "dia_mes_colheita"]]

    nome_pasta = paste0(name, "_", dia_mes, "_", mes_plantio, "_", dia_colheita, "_", mes_colheita)

    # Correção da correspondência entre DAS x DAP
    x = dplyr::mutate(x, DAS = DAS + 1)

    # Salvar
    join_with_existing(x, nome_pasta, file)
  }

  else if((stringr::str_remove(file, ".OUT")) == "SoilWat"){

    # Pegar informações do diretório de Outputs
    information = read.csv(here("Outputs",
                                "auxiliar.csv"))

    mes_plantio = information[[i, "mes_plantio"]]
    dia_mes = information[[i, "dia_mes"]]
    mes_colheita = information[[i, "mes_colheita"]]
    dia_colheita = information[[i, "dia_mes_colheita"]]

    nome_pasta = paste0(name, "_", dia_mes, "_", mes_plantio, "_", dia_colheita, "_", mes_colheita)

    # Pegar e Salvar informação sobre irrigação
    information[i, "water"] = dplyr::last(x$IRRC)

    write.table(information,
                here("Outputs", "auxiliar.csv"),
                row.names = F,
                sep = ",")

    # Salvar
    join_with_existing(x, nome_pasta, file)
  }

  else if((stringr::str_remove(file, ".OUT")) == "ET"){

    # Pegar informações do diretório de Outputs
    information = read.csv(here("Outputs",
                                "auxiliar.csv"))

    mes_plantio = information[[i, "mes_plantio"]]
    dia_mes = information[[i, "dia_mes"]]
    mes_colheita = information[[i, "mes_colheita"]]
    dia_colheita = information[[i, "dia_mes_colheita"]]

    nome_pasta = paste0(name, "_", dia_mes, "_", mes_plantio, "_", dia_colheita, "_", mes_colheita)
    # Salvar
    join_with_existing(x, nome_pasta, file)
  }

  else if((stringr::str_remove(file,".OUT")) == "PlantGr2"){

    # Pegar informações do diretório de Outputs
    information = read.csv(here("Outputs",
                                "auxiliar.csv"))

    mes_plantio = information[[i, "mes_plantio"]]
    dia_mes = information[[i, "dia_mes"]]
    mes_colheita = information[[i, "mes_colheita"]]
    dia_colheita = information[[i, "dia_mes_colheita"]]

    nome_pasta = paste0(name, "_", dia_mes, "_", mes_plantio, "_", dia_colheita, "_", mes_colheita)

    # Correção da correspondência entre DAS x DAP
    x = dplyr::mutate(x, DAS = DAS + 1)

    # Salvar
    join_with_existing(x, nome_pasta, file)
  }
}







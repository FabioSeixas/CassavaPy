
identify_out = function(file){

  vec = c("Weather" = 10, "PlantGro" = 10, "PlantGrf" = 11,
          "SoilWat" = 12, "PlantGr2" = 10, "ET" = 12)

  return(vec[stringr::str_remove(file,".OUT")])
}

nrow_fun = function(index_vec, i, file){

  if(is.na(index_vec[i + 1])){
    return(-1)
  }
  else{
    between_rows = identify_out(file)
    start = index_vec[i]
    end = index_vec[i + 1] - between_rows
    return(end - start)
  }
}

join_with_existing = function(data, nome_pasta, file){

  # Essa função:
  # 1) carrega a tabela de resultados já salvos de cada simulação (SimResults.csv)
  # 2) Faz o join com os resultados/output atual
  # 3) Salva o resultado do join como ''SimResults.csv''

  # 1) Carregar SimResults.csv
  previous_data = read.csv(here("Outputs", nome_pasta,
                       "SimResults.csv"))

  # 2) JOIN
  # O output Weather.OUT é o que possui o maior número de linhas, porque
  # começa no DAS = 0 e só termina na data de colheita. Por isso, ele deve
  # ser a referência para a quantidade de linhas em SimResults.csv

  if((stringr::str_remove(file,".OUT")) == "Weather"){

    q = dplyr::right_join(previous_data, data, by = "DAS")
  }
  else{
    q = dplyr::left_join(previous_data, data, by = "DAS")
  }

  # 3) Salvar resultado do Join
  write.csv(q, here("Outputs",
                    nome_pasta,
                    "SimResults.csv"), row.names = F)
}

fazer_data = function(doy, year){

  return(as.Date(doy,
                 origin = paste0(year, "-01-01")))
}

data_plantio = function(x){

  sub_x = dplyr::select(x, date, DAP)
  sub_x = dplyr::filter(sub_x, !is.na(DAP))

  return(sub_x[[1, "date"]])
}

data_colheita = function(x){

  sub_x = dplyr::select(x, date, DAP)
  sub_x = dplyr::filter(sub_x, !is.na(DAP))
  sub_x = dplyr::pull(sub_x, date)

  return(dplyr::last(sub_x))
}

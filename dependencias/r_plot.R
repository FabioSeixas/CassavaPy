library(datasets)
library(here)

# Pegar inputs da função plot_R (Python)
args = commandArgs(trailingOnly = TRUE)
n_trat = as.numeric(args[1])
directories = args[2:(n_trat + 1)]


# Dicionário com os códigos das variáveis e suas legendas
dic_vars = source(here("dependencias",
                       "vars_dictionary.R"))$value

source(here("dependencias",
            "r_functions.R"))$value


# Funções para geração dos gráficos
water = function(data, dic_vars, directory){

  jpeg(here("Outputs",
            directory,
            "water.jpg"),
       width = 2500, height = 2000, res = 300)

  par(mfrow = c(2, 3))

  with(data, {

      for(i in 1:6){ # 1:6 porque os 6 primeiros elementos do
                     # dicionário serão plotados através
                     # dessa função

        plot(x = date,
             y = data[[names(dic_vars)[[i]]]],
             main = dic_vars[[i]],
             ylab = dic_vars[[i]],
             frame = FALSE,
             type = "l",
             xaxt = "n",
             xlab = "")
        axis(1, x$date, format(x$date, "%b"),
             cex.axis = 1, tick = F)

      }

    title(paste("Local:", nome, "      ",
                "Plantio:", format(plantio,"%d %B %Y"), "      ",
                "Colheita:", format(colheita, "%d %B %Y")),
          line = -25, outer = TRUE)
  })

  dev.off()
}

plant_water = function(data, dic_vars, directory){

  jpeg(here("Outputs",
            directory,
            "plant_water.jpg"),
       width = 2500, height = 2000, res = 300)

  par(mfrow = c(2, 3))

  with(data, {

    for(i in 7:12){# 7:12 porque são os 6 elementos do
                   # dicionário que serão plotados através
                   # dessa função

      plot(x = date,
           y = data[[names(dic_vars)[[i]]]],
           main = dic_vars[[i]],
           ylab = dic_vars[[i]],
           xlab = "",
           frame = FALSE,
           type = "l",
           xaxt = "n")
      axis(1, x$date, format(x$date, "%b"),
           cex.axis = 1, tick = F)

    }

    title(paste("Local:", nome, "      ",
                "Plantio:", format(plantio,"%d %B %Y"), "      ",
                "Colheita:", format(colheita, "%d %B %Y")),
          line = -25, outer = TRUE)
  })

  dev.off()
}

roots_soil = function(data, dic_vars, directory){

  color_vector = c("purple", "yellow", "green", "black")

  jpeg(here("Outputs",
            directory,
            "roots_soil.jpg"),
       width = 2500, height = 2000, res = 300)

  par(mfrow = c(2, 1))
  par(mar = rep(5, 4))

  # Root Density
  with(x, {
    plot(date,
         y = data[[names(dic_vars)[[13]]]],
         main = expression(Root~Density~by~Soil~Layer~cm~cm^{-3}),
         ylab = expression(Root~Density~cm~cm^{-3}),
         xlab = "",
         frame = FALSE,
         type = "l",
         col = "blue",
         xaxt = "n")
    axis(1, x$date, format(x$date, "%b"),
         cex.axis = 1, tick = F)

    for(n in 14:17){
      lines(date,
            y = data[[names(dic_vars)[[n]]]],
            xlab = "",
            type = "l",
            col = color_vector[n - 13])
      axis(1, x$date, format(x$date, "%b"),
           cex.axis = 1, tick = F)
    }

    legend("topleft",
           col = c("blue", color_vector),
           lty = rep(1, 5),
           legend = c("Layer 1", "Layer 2",
                      "Layer 3", "Layer 4",
                      "Layer 5"), cex = 0.7, lwd = 4)
  })

  # Soil Water by Layer
  with(x, {
    plot(date,
         y = data[[names(dic_vars)[[18]]]],
         main = expression(Soil~Water~by~Layer~cm^{3}~cm^{-3}),
         ylab = expression(Soil~Water~by~Layer~cm^{3}~cm^{-3}),
         xlab = "",
         frame = FALSE,
         type = "l",
         col = "blue",
         xaxt = "n")
    axis(1, x$date, format(x$date, "%b"),
         cex.axis = 1, tick = F)

    for(n in 19:22){
      lines(date,
            y = data[[names(dic_vars)[[n]]]],
            xlab = "",
            type = "l",
            col = color_vector[n - 18])
      axis(1, x$date, format(x$date, "%b"),
           cex.axis = 1, tick = F)
    }

    legend("bottomleft",
           col = c("blue", color_vector),
           lty = rep(1, 5),
           legend = c("Layer 1", "Layer 2",
                      "Layer 3", "Layer 4",
                      "Layer 5"), cex = .7, lwd = 4,
           box.lty = 0)

    title(paste("Local:", nome, "      ",
                "Plantio:", format(plantio,"%d %B %Y"), "      ",
                "Colheita:", format(colheita, "%d %B %Y")),
          line = -17, outer = TRUE)
  })


  dev.off()
}

yield = function(data, dic_vars, directory){

  jpeg(here("Outputs",
            directory,
            "yield.jpg"),
       width = 2500, height = 2000, res = 300)

  par(mfrow = c(2, 3))

  with(data, {

    for(i in 23:27){# 23:27 porque são os 5 elementos do
                    # dicionário que serão plotados através
                    # dessa função

      plot(x = date,
           y = data[[names(dic_vars)[[i]]]],
           main = dic_vars[[i]],
           ylab = dic_vars[[i]],
           xlab = "",
           frame = FALSE,
           type = "l",
           xaxt = "n")
      axis(1, x$date, format(x$date, "%b"),
           cex.axis = 1, tick = F)

    }

    title(paste("Local:", nome, "      ",
                "Plantio:", format(plantio,"%d %B %Y"), "      ",
                "Colheita:", format(colheita, "%d %B %Y")),
          line = -25, outer = TRUE)

  })

  dev.off()
}


# Aplicar loop - Um para cada pasta de resultado
for(directory in directories){

  # Carregar dados
  x = read.csv(here("Outputs",
                directory,
                "SimResults.csv"))

  # Criar uma coluna correspondente a data
  x = dplyr::mutate(x, date = fazer_data(DOY.y, X.YEAR.y))

  # Pegar nome (localidade)
  nome = stringr::str_split(directory, "_")[[1]][1]

  # Pegar datas
  plantio = data_plantio(x)

  colheita = data_colheita(x)

  # Rodar produção de gráficos
  water(x, dic_vars, directory)

  plant_water(x, dic_vars, directory)

  roots_soil(x, dic_vars, directory)

  yield(x, dic_vars, directory)

}




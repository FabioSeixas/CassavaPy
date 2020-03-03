# Dicionário de códigos das variáveis e respectivas descrições
# Para uso nos gráficos

# OBS: Alguns nomes de variáveis estão com '.x' no final
# Acontece que no join the todas as variáveis, algumas são
# repetidas, e o R coloca esse '.x' para não ficarem
# colunas com mesmo nome.
# Se o padrão se manter, não há problema.

c(# 1) Distribuição da disponibilidade de água ao longo do ano
  "PRED" = "Rain (mm)",
  "PREC" = "Cumulative Precipitation (mm)",
  "SWTD" = "Total Soil Water in Profile (mm)",
  "SWXD" = "Extractable Water in Profile (mm)",
  "DRNC" = "Cumulative Drainage (mm)",
  "ROFC" = "Cumulative Runoff (mm)",

  # 2) Variáveis Planta x Água
  "EPAA" = "Plant Transpiration (mm/d)",
  "SWXD.x" = "Extractable Water by Roots (mm)",
  "WAVRD.x" = "Water Available to Demand Ratio",
  "ETAA" = "Evapotranspiration (mm/d)",
  "LAID.x" = "Leaf Area Index",
  "AWAD" = expression(Assimilate~Production~kg~ha^{-1}~day^{-1}),
  
  # 3) Distribuição de Raízes e Água no Perfil
  "RL1D" = "Root Density in Soil Layer 1",
  "RL2D" = "Root Density in Soil Layer 2",
  "RL3D" = "Root Density in Soil Layer 3",
  "RL4D" = "Root Density in Soil Layer 4",
  "RL5D" = "Root Density in Soil Layer 5",
  "SW1D" = "Soil Water in Layer 1 (mm)",
  "SW2D" = "Soil Water in Layer 2 (mm)",
  "SW3D" = "Soil Water in Layer 3 (mm)",
  "SW4D" = "Soil Water in Layer 4 (mm)",
  "SW5D" = "Soil Water in Layer 5 (mm)",
  
  # 4) Produção
  "RWAD" = expression(Root~Weight~kg[dm]~ha^{-1}),
  "CWAD" = expression(Tops~Weight~kg[dm]~ha^{-1}),
  "HWAD" = expression(Harvest~Product~kg[dm]~ha^{-1}),
  "HIAD" = expression(Harvest~Index~(root/top)),
  "RSWAD" = expression(Reserves~Weight~kg~ha^{-1}))

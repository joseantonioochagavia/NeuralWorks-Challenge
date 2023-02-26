-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.body   = '{"MES": 4, "temporada_alta": 0, "DIA_Jueves": 0, "DIA_Domingo": 1, "DIA_Lunes": 0, "DIA_Miercoles": 0, "OPERA_Grupo LATAM": 1, "periodo_dia_tarde": 0, "DIA_Martes": 0, "DIA_Viernes": 0, "periodo_dia_mañana": 0, "DIA_Sabado": 0, "periodo_dia_noche": 1, "OPERA_Sky Airline": 0, "OPERA_Latin American Wings": 0, "DES_Buenos Aires": 0, "DES_Puerto Montt": 0, "DES_Lima": 0, "DES_Iquique": 0, "OPERA_Air Canada": 0}'
wrk.headers["Content-Type"] = "application/json"
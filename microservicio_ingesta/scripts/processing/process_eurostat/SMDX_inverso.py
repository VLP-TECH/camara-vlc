def invertir_decodificacion_sdmx(json_completo):

    datos_sdmx = json_completo['value']
    orden_dimensiones = json_completo['id']
    tamanno_dimensiones = json_completo['size']

    resultados = []
    for clave, valor in datos_sdmx.items():
        indice = 0
        indices = {}
        for i in reversed(tamanno_dimensiones):
            indice -= 1
            resultado = int(clave) % i

            guion = json_completo['dimension'][orden_dimensiones[indice]]['category']['index']

            for ref, val in guion.items():
                if val == resultado:
                    index = ref
            
            etiqueta = json_completo['dimension'][orden_dimensiones[indice]]['category']['label'][index]

            indices[orden_dimensiones[indice]] = etiqueta
            
            clave = int(clave) // i

        indices['resultado'] = valor
        resultados.append(indices)

    return resultados
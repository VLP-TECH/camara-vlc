from pathlib import Path
import aiofiles

class FileWriter:
    output: Path
    nombre_variable: str
    _file_handler = None
    CONTENIDO_INICIO = """# -*- coding: utf-8 -*-
# ¡ATENCIÓN! ESTE ARCHIVO ES GENERADO AUTOMÁTICAMENTE.
# NO LO EDITES A MANO. 
    """

    def __init__(self, output, nombre_variable):
        self.output = output
        self.nombre_variable = nombre_variable


    async def __aenter__(self):
        '''
        Se ejecuta al entrar en el bloque async with
        Abre el archivo de forma asíncrona y escribe la cabecera
        '''
        self._file_handler = await aiofiles.open(self.output, 'w', encoding='utf-8')

        await self._file_handler.write(self.CONTENIDO_INICIO)
        await self._file_handler.write(f'\n\n{self.nombre_variable} = [\n')

        return self

    async def __aexit__(self, a, b, c):
        '''
        Se ejecuta al salir del bloque async with
        Escribe el final y cierra el archivo
        '''
        await self._file_handler.write(']')
        await self._file_handler.close()
        print(f"Fichero generado y cerrado correctamente en: {self.output}")


    async def agregar_elemento(self, elemento):
        if elemento:
            linea_formateada = f"    {elemento},\n"
            await self._file_handler.write(linea_formateada)

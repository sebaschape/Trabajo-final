
import datetime
import csv
import os
import platform
import time
import re

class ParqueaderoChopiplu:
    def __init__(self):
        self.usuarios = {}  
        self.vehiculos_activos = {}  
        self.historial_vehiculos = []  
        self.administradores = {
            "admin": "adminchopiplu"
        }
        self.espacios_totales = 64
        self.tarifa_hora = 7000
        self.tarifa_cuarto = 1500
        self.log_eventos = []
        
    def log_evento(self, accion, tiempo_inicio):
        
        tiempo_fin = time.time()
        tiempo_operacion = (tiempo_fin - tiempo_inicio) * 1000  # en milisegundos
        
        timestamp = datetime.datetime.now()
        evento = {
            'fecha_hora': timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            'accion': accion,
            'tiempo_ms': round(tiempo_operacion, 3),
            'usuario_sistema': os.getenv('USERNAME', 'desconocido'),
            'so': platform.system(),
            'plataforma': platform.platform()
        }
        self.log_eventos.append(evento)
    
    def validar_nombre(self, nombre):
        
        errores = []
        if len(nombre) < 3:
            errores.append("El nombre debe tener al menos 3 caracteres")
        if any(char.isdigit() for char in nombre):
            errores.append("El nombre no puede contener números")
        if not nombre.replace(' ', '').isalpha():
            errores.append("El nombre solo puede contener letras")
        return errores
    
    def validar_documento(self, documento):
        
        errores = []
        if not documento.isdigit():
            errores.append("El documento solo puede contener números")
        elif not (3 <= len(documento) <= 15):
            errores.append("El documento debe tener entre 3 y 15 dígitos")
        return errores
    
    def validar_placa(self, placa):
        
        errores = []
        if len(placa) != 6:
            errores.append("La placa debe tener exactamente 6 caracteres")
        elif not re.match(r'^[A-Za-z]{3}[0-9]{3}$', placa):
            errores.append("La placa debe tener 3 letras seguidas de 3 números (ej: ABC123)")
        return errores
    
    def registrar_usuario(self):
        
        tiempo_inicio = time.time()
        print("\n=== REGISTRO DE USUARIO ===")
        
        while True:
            nombre = input("Ingrese el nombre: ").strip()
            errores = self.validar_nombre(nombre)
            if not errores:
                break
            print("Errores encontrados:")
            for error in errores:
                print(f"- {error}")
        
        while True:
            apellido = input("Ingrese el apellido: ").strip()
            errores = self.validar_nombre(apellido)
            if not errores:
                break
            print("Errores encontrados:")
            for error in errores:
                print(f"- {error}")
        
        while True:
            documento = input("Ingrese el documento: ").strip()
            errores = self.validar_documento(documento)
            if errores:
                print("Errores encontrados:")
                for error in errores:
                    print(f"- {error}")
            elif documento in self.usuarios:
                print("Error: El documento ya está registrado")
            else:
                break
        
        while True:
            placa = input("Ingrese la placa del vehículo: ").strip().upper()
            errores = self.validar_placa(placa)
            if errores:
                print("Errores encontrados:")
                for error in errores:
                    print(f"- {error}")
            else:
                
                placa_existente = False
                for doc, usuario in self.usuarios.items():
                    if usuario['placa'] == placa:
                        placa_existente = True
                        break
                
                if placa_existente:
                    print("Error: La placa ya está registrada")
                else:
                    break
        
        self.usuarios[documento] = {
            'nombre': nombre,
            'apellido': apellido,
            'placa': placa
        }
        
        print(f"\n✓ Usuario registrado exitosamente:")
        print(f"  Nombre: {nombre} {apellido}")
        print(f"  Documento: {documento}")
        print(f"  Placa: {placa}")
        
        self.log_evento("Registro de usuario", tiempo_inicio)
    
    def ingresar_vehiculo(self):
        
        tiempo_inicio = time.time()
        print("\n=== INGRESO DE VEHÍCULO ===")
        
        if len(self.vehiculos_activos) >= self.espacios_totales:
            print("❌ El parqueadero está lleno. No hay espacios disponibles.")
            return
        
        placa = input("Ingrese la placa del vehículo: ").strip().upper()
        
        
        documento = None
        usuario = None
        for doc, user in self.usuarios.items():
            if user['placa'] == placa:
                documento = doc
                usuario = user
                break
        
        if not usuario:
            print("❌ Placa no registrada. Debe registrar el usuario primero.")
            return
        
        if placa in self.vehiculos_activos:
            print("❌ El vehículo ya se encuentra en el parqueadero.")
            return
        
        hora_ingreso = datetime.datetime.now()
        self.vehiculos_activos[placa] = {
            'usuario': usuario,
            'documento': documento,
            'hora_ingreso': hora_ingreso
        }
        
        print(f"\n✓ Vehículo ingresado exitosamente:")
        print(f"  Usuario: {usuario['nombre']} {usuario['apellido']}")
        print(f"  Placa: {placa}")
        print(f"  Hora de ingreso: {hora_ingreso.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Espacios ocupados: {len(self.vehiculos_activos)}/{self.espacios_totales}")
        
        
        self.generar_recibo_ingreso(usuario, placa, hora_ingreso)
        
        self.log_evento("Ingreso de vehículo", tiempo_inicio)
    
    def generar_recibo_ingreso(self, usuario, placa, hora_ingreso):
        
        print("\n" + "="*50)
        print("           RECIBO DE INGRESO")
        print("        PARQUEADERO LOS CHOPIPLU")
        print("="*50)
        print(f"Usuario: {usuario['nombre']} {usuario['apellido']}")
        print(f"Documento: {self.get_documento_by_placa(placa)}")
        print(f"Placa: {placa}")
        print(f"Fecha: {hora_ingreso.strftime('%Y-%m-%d')}")
        print(f"Hora: {hora_ingreso.strftime('%H:%M:%S')}")
        print("-"*50)
        print("Conserve este recibo para el retiro")
        print("Tarifa: $7,000 por hora o fracción")
        print("Pago mínimo: $7,000")
        print("="*50)
    
    def get_documento_by_placa(self, placa):
        
        for doc, usuario in self.usuarios.items():
            if usuario['placa'] == placa:
                return doc
        return None
    
    def calcular_costo(self, hora_ingreso, hora_salida):
        
        tiempo_total = hora_salida - hora_ingreso
        minutos_totales = tiempo_total.total_seconds() / 60
        
        horas_completas = int(minutos_totales // 60)
        minutos_restantes = int(minutos_totales % 60)
        
        
        cuartos_hora = 0
        if minutos_restantes > 0:
            cuartos_hora = (minutos_restantes + 14) // 15  
        
        costo_horas = horas_completas * self.tarifa_hora
        costo_cuartos = cuartos_hora * self.tarifa_cuarto
        total = costo_horas + costo_cuartos
        
        
        if total < self.tarifa_hora:
            total = self.tarifa_hora
        
        return {
            'horas': horas_completas,
            'cuartos': cuartos_hora,
            'minutos_restantes': minutos_restantes,
            'costo_horas': costo_horas,
            'costo_cuartos': costo_cuartos,
            'total': total,
            'tiempo_total_minutos': int(minutos_totales)
        }
    
    def retirar_vehiculo(self):
        """Registra el retiro de un vehículo del parqueadero"""
        tiempo_inicio = time.time()
        print("\n=== RETIRO DE VEHÍCULO ===")
        
        if not self.vehiculos_activos:
            print("❌ No hay vehículos en el parqueadero.")
            return
        
        placa = input("Ingrese la placa del vehículo: ").strip().upper()
        
        if placa not in self.vehiculos_activos:
            print("❌ El vehículo no se encuentra en el parqueadero.")
            return
        
        vehiculo = self.vehiculos_activos[placa]
        hora_salida = datetime.datetime.now()
        
        
        calculo = self.calcular_costo(vehiculo['hora_ingreso'], hora_salida)
        
        
        self.generar_factura(vehiculo, hora_salida, calculo)
        
        
        registro_historial = {
            'usuario': vehiculo['usuario'],
            'documento': vehiculo['documento'],
            'placa': placa,
            'hora_ingreso': vehiculo['hora_ingreso'],
            'hora_salida': hora_salida,
            'tiempo_minutos': calculo['tiempo_total_minutos'],
            'total_pagado': calculo['total']
        }
        self.historial_vehiculos.append(registro_historial)
        
        
        del self.vehiculos_activos[placa]
        
        print(f"\n✓ Vehículo retirado exitosamente.")
        print(f"  Espacios ocupados: {len(self.vehiculos_activos)}/{self.espacios_totales}")
        
        self.log_evento("Retiro de vehículo", tiempo_inicio)
    
    def generar_factura(self, vehiculo, hora_salida, calculo):
        
        print("\n" + "="*50)
        print("              FACTURA DE PAGO")
        print("           PARQUEADERO LOS CHOPIPLU")
        print("="*50)
        print(f"Usuario: {vehiculo['usuario']['nombre']} {vehiculo['usuario']['apellido']}")
        print(f"Documento: {vehiculo['documento']}")
        print(f"Placa: {vehiculo['usuario']['placa']}")
        print("-"*50)
        print(f"Ingreso: {vehiculo['hora_ingreso'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Salida:  {hora_salida.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tiempo total: {calculo['tiempo_total_minutos']} minutos")
        print("-"*50)
        print("DETALLE DE COBRO:")
        print(f"Horas completas: {calculo['horas']} x ${self.tarifa_hora:,} = ${calculo['costo_horas']:,}")
        print(f"Cuartos de hora: {calculo['cuartos']} x ${self.tarifa_cuarto:,} = ${calculo['costo_cuartos']:,}")
        if calculo['total'] == self.tarifa_hora and (calculo['costo_horas'] + calculo['costo_cuartos']) < self.tarifa_hora:
            print(f"Pago mínimo aplicado: ${self.tarifa_hora:,}")
        print("-"*50)
        print(f"TOTAL A PAGAR: ${calculo['total']:,}")
        print("="*50)
        print("Gracias por usar nuestro servicio")
        print("="*50)
    
    def autenticar_admin(self):
        
        print("\n=== ACCESO ADMINISTRADOR ===")
        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()
        
        return usuario in self.administradores and self.administradores[usuario] == contraseña
    
    def menu_administrador(self):
        
        tiempo_inicio = time.time()
        
        if not self.autenticar_admin():
            print("❌ Credenciales incorrectas.")
            return
        
        while True:
            print("\n=== PANEL ADMINISTRADOR ===")
            print("1. Total de vehículos registrados")
            print("2. Total de vehículos retirados")
            print("3. Total de vehículos sin retirar")
            print("4. Total pago de vehículos retirados")
            print("5. Tiempo promedio de estancia")
            print("6. Lista de usuarios")
            print("7. Vehículo con tiempo máximo y mínimo")
            print("8. Exportar reportes a CSV")
            print("9. Ver log de eventos")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.reporte_vehiculos_registrados()
            elif opcion == "2":
                self.reporte_vehiculos_retirados()
            elif opcion == "3":
                self.reporte_vehiculos_activos()
            elif opcion == "4":
                self.reporte_total_pagos()
            elif opcion == "5":
                self.reporte_tiempo_promedio()
            elif opcion == "6":
                self.reporte_lista_usuarios()
            elif opcion == "7":
                self.reporte_tiempos_extremos()
            elif opcion == "8":
                self.exportar_csv()
            elif opcion == "9":
                self.mostrar_log_eventos()
            elif opcion == "0":
                break
            else:
                print("❌ Opción inválida.")
        
        self.log_evento("Sesión administrador", tiempo_inicio)
    
    def reporte_vehiculos_registrados(self):
        
        total = len(self.usuarios)
        print(f"\n📊 Total de vehículos registrados: {total}")
    
    def reporte_vehiculos_retirados(self):
        
        total = len(self.historial_vehiculos)
        print(f"\n📊 Total de vehículos retirados: {total}")
    
    def reporte_vehiculos_activos(self):
        
        total = len(self.vehiculos_activos)
        print(f"\n📊 Total de vehículos sin retirar: {total}")
        if total > 0:
            print("\nVehículos actualmente en el parqueadero:")
            for placa, info in self.vehiculos_activos.items():
                tiempo_actual = datetime.datetime.now()
                tiempo_estancia = tiempo_actual - info['hora_ingreso']
                minutos = int(tiempo_estancia.total_seconds() / 60)
                print(f"- {placa}: {info['usuario']['nombre']} {info['usuario']['apellido']} ({minutos} min)")
    
    def reporte_total_pagos(self):
        
        total = sum(vehiculo['total_pagado'] for vehiculo in self.historial_vehiculos)
        print(f"\n💰 Total pagado por vehículos retirados: ${total:,}")
    
    def reporte_tiempo_promedio(self):
        
        if not self.historial_vehiculos:
            print("\n📊 No hay datos de vehículos retirados.")
            return
        
        total_minutos = sum(vehiculo['tiempo_minutos'] for vehiculo in self.historial_vehiculos)
        promedio = total_minutos / len(self.historial_vehiculos)
        horas = int(promedio // 60)
        minutos = int(promedio % 60)
        
        print(f"\n⏱️ Tiempo promedio de estancia: {horas}h {minutos}m ({promedio:.1f} minutos)")
    
    def reporte_lista_usuarios(self):
        
        print(f"\n👥 Lista de usuarios registrados ({len(self.usuarios)}):")
        print("-" * 60)
        for doc, usuario in self.usuarios.items():
            print(f"Doc: {doc} | {usuario['nombre']} {usuario['apellido']} | Placa: {usuario['placa']}")
    
    def reporte_tiempos_extremos(self):
        
        if not self.historial_vehiculos:
            print("\n📊 No hay datos de vehículos retirados.")
            return
        
        vehiculo_max = max(self.historial_vehiculos, key=lambda x: x['tiempo_minutos'])
        vehiculo_min = min(self.historial_vehiculos, key=lambda x: x['tiempo_minutos'])
        
        print(f"\n🔝 Vehículo con mayor tiempo de estancia:")
        self.mostrar_info_vehiculo(vehiculo_max)
        
        print(f"\n🔻 Vehículo con menor tiempo de estancia:")
        self.mostrar_info_vehiculo(vehiculo_min)
    
    def mostrar_info_vehiculo(self, vehiculo):
        
        horas = vehiculo['tiempo_minutos'] // 60
        minutos = vehiculo['tiempo_minutos'] % 60
        print(f"   Placa: {vehiculo['placa']}")
        print(f"   Usuario: {vehiculo['usuario']['nombre']} {vehiculo['usuario']['apellido']}")
        print(f"   Tiempo: {horas}h {minutos}m")
        print(f"   Total pagado: ${vehiculo['total_pagado']:,}")
    
    def exportar_csv(self):
        
        tiempo_inicio = time.time()
        
        try:
            
            if not os.path.exists('reportes'):
                os.makedirs('reportes')
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            
            with open(f'reportes/usuarios_{timestamp}.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Documento', 'Nombre', 'Apellido', 'Placa'])
                for doc, usuario in self.usuarios.items():
                    writer.writerow([doc, usuario['nombre'], usuario['apellido'], usuario['placa']])
            
            
            with open(f'reportes/historial_{timestamp}.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Documento', 'Nombre', 'Apellido', 'Placa', 'Hora_Ingreso', 
                               'Hora_Salida', 'Tiempo_Minutos', 'Total_Pagado'])
                for vehiculo in self.historial_vehiculos:
                    writer.writerow([
                        vehiculo['documento'],
                        vehiculo['usuario']['nombre'],
                        vehiculo['usuario']['apellido'],
                        vehiculo['placa'],
                        vehiculo['hora_ingreso'].strftime('%Y-%m-%d %H:%M:%S'),
                        vehiculo['hora_salida'].strftime('%Y-%m-%d %H:%M:%S'),
                        vehiculo['tiempo_minutos'],
                        vehiculo['total_pagado']
                    ])
            
            
            with open(f'reportes/activos_{timestamp}.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Documento', 'Nombre', 'Apellido', 'Placa', 'Hora_Ingreso'])
                for placa, info in self.vehiculos_activos.items():
                    writer.writerow([
                        info['documento'],
                        info['usuario']['nombre'],
                        info['usuario']['apellido'],
                        placa,
                        info['hora_ingreso'].strftime('%Y-%m-%d %H:%M:%S')
                    ])
            
            print(f"\n✅ Reportes exportados exitosamente en la carpeta 'reportes'")
            print(f"   - usuarios_{timestamp}.csv")
            print(f"   - historial_{timestamp}.csv")
            print(f"   - activos_{timestamp}.csv")
            
        except Exception as e:
            print(f"❌ Error al exportar: {e}")
        
        self.log_evento("Exportar CSV", tiempo_inicio)
    
    def mostrar_log_eventos(self):
        
        if not self.log_eventos:
            print("\n📝 No hay eventos registrados.")
            return
        
        print(f"\n📝 LOG DE EVENTOS DEL SISTEMA")
        print(f"Usuario del sistema: {os.getenv('USERNAME', 'desconocido')}")
        print(f"Sistema operativo: {platform.system()}")
        print(f"Plataforma: {platform.platform()}")
        print(f"Total de eventos: {len(self.log_eventos)}")
        print("-" * 80)
        
        for evento in self.log_eventos:
            print(f"{evento['fecha_hora']} | {evento['accion']} | {evento['tiempo_ms']}ms")
    
    def menu_principal(self):
        
        print("🚗 BIENVENIDO AL SISTEMA DE PARQUEADERO LOS CHOPIPLU 🚗")
        
        while True:
            print("\n" + "="*50)
            print("      PARQUEADERO LOS CHOPIPLU - MENÚ PRINCIPAL")
            print("="*50)
            print("1. Registrar Usuario")
            print("2. Ingresar Vehículo")
            print("3. Retirar Vehículo")
            print("4. Administrador")
            print("5. Salir")
            print("="*50)
            print(f"Espacios ocupados: {len(self.vehiculos_activos)}/{self.espacios_totales}")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.ingresar_vehiculo()
            elif opcion == "3":
                self.retirar_vehiculo()
            elif opcion == "4":
                self.menu_administrador()
            elif opcion == "5":
                print("\n👋 ¡Gracias por usar el Sistema de Parqueadero Los Chopiplu!")
                
                if self.log_eventos:
                    print(f"Total de operaciones realizadas: {len(self.log_eventos)}")
                break
            else:
                print("❌ Opción inválida. Por favor seleccione una opción válida.")

def main():
    
    try:
        sistema = ParqueaderoChopiplu()
        sistema.menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Sistema cerrado por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
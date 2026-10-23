CREATE DATABASE IF NOT EXISTS DB_SUCIA;
USE DB_SUCIA;
CREATE TABLE transacciones_sucias (
        id_transaccion INT,
        rut VARCHAR(20),
        sku VARCHAR(50),
        canal_venta VARCHAR(50),
        fecha_str VARCHAR(50),
        tienda_origen VARCHAR(50),
        cantidad INT,
        monto DECIMAL(12,2)
    );
INSERT INTO transacciones_sucias VALUES (7001, '145350-3', 'TELEFONO_X', 'Call Center', '2026.10.01', '101', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7002, '199658-6', 'TELEFONO_X', 'TIENDA FISICA', '2026-10-01 14:30:00', '103', 2, -50000);
INSERT INTO transacciones_sucias VALUES (7003, '191214-0', 'NOTEBOOK-HP', 'Call Center', '01-10-2026', NULL, 3, 12000);
INSERT INTO transacciones_sucias VALUES (7004, '122467-5', 'NOTE-HP', 'app_movil', '2026/10/01', 'N/A', -100, -100);
INSERT INTO transacciones_sucias VALUES (7005, '191214-0', 'NOTEBOOK-HP', 'web', '2026-10-01 14:30:00', '106', 3, -100);
INSERT INTO transacciones_sucias VALUES (7006, '183296-1', 'sku-002', 'APP', '2026/10/01', 'N/A', -100, 30000);
INSERT INTO transacciones_sucias VALUES (7007, '114130-1', 'SKU-003', 'call-center', '2026-10-01', '104', -100, -100);
INSERT INTO transacciones_sucias VALUES (7008, '130479-5', 'sku_1', 'Tienda_Fisica', '01/10/2026', '106', 3, -50000);
INSERT INTO transacciones_sucias VALUES (7009, '130814-6', 'tel-x', 'app_movil', '01-10-2026', '104', 1, -50000);
INSERT INTO transacciones_sucias VALUES (7010, '122467-5', 'sku_1', NULL, '2026.10.01', 'Sin Asignar', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7011, '115777-3', 'PROD-A', 'Tienda_Fisica', '2026/10/01', NULL, 2, 12000);
INSERT INTO transacciones_sucias VALUES (7012, '114130-1', 'SKU-003', 'TIENDA FISICA', '2026-10-01', '102', 1, -100);
INSERT INTO transacciones_sucias VALUES (7013, '137881-5', 'SKU-003', NULL, '01/10/2026', '106', -5, 30000);
INSERT INTO transacciones_sucias VALUES (7014, '130479-5', 'SKU-002', 'TIENDA FISICA', '01/10/2026', '102', 3, -100);
INSERT INTO transacciones_sucias VALUES (7015, '147949-K', 'tel-x', 'APP', '2026.10.01', '101', 2, -50000);
INSERT INTO transacciones_sucias VALUES (7016, '199658-6', 'NOTEBOOK-HP', 'call-center', '2026/10/01', '101', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7017, '127854-1', 'sku_1', NULL, '2026.10.01', NULL, 3, -100);
INSERT INTO transacciones_sucias VALUES (7018, '168649-1', 'NOTE-HP', 'Web', '01/10/2026', '106', 1, 30000);
INSERT INTO transacciones_sucias VALUES (7019, '158180-8', 'NOTEBOOK-HP', NULL, '01-10-2026', '101', 3, -50000);
INSERT INTO transacciones_sucias VALUES (7020, '122489-4', 'SKU-002', 'web', '2026.10.01', NULL, -100, 12000);
INSERT INTO transacciones_sucias VALUES (7021, '183296-1', 'NOTEBOOK-HP', 'call-center', '2026.10.01', NULL, -5, 12000);
INSERT INTO transacciones_sucias VALUES (7022, '145928-0', 'SKU-002', 'APP', '01/10/2026', 'N/A', 2, -50000);
INSERT INTO transacciones_sucias VALUES (7023, '122489-4', 'SKU-002', 'web', '2026-10-01 14:30:00', '102', -5, -100);
INSERT INTO transacciones_sucias VALUES (7024, '199658-6', 'tel-x', NULL, '01-10-2026', '104', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7025, '199799-K', 'SKU-002', 'APP', '2026-10-01', 'N/A', 1, -50000);
INSERT INTO transacciones_sucias VALUES (7026, '199658-6', 'NOTE-HP', 'Call Center', '2026-10-01', '104', 1, -50000);
INSERT INTO transacciones_sucias VALUES (7027, '147949-K', 'sku-002', NULL, '2026-10-01 14:30:00', '101', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7028, '114130-1', 'TELEFONO_X', 'app_movil', '01/10/2026', 'Sin Asignar', 1, 12000);
INSERT INTO transacciones_sucias VALUES (7029, '121704-6', 'sku_1', 'APP', '2026/10/01', NULL, -5, -50000);
INSERT INTO transacciones_sucias VALUES (7030, '189982-5', 'SKU-002', NULL, '01-10-2026', '106', 3, 12000);
INSERT INTO transacciones_sucias VALUES (7031, '114130-1', 'PROD-A', NULL, '01-10-2026', '105', -100, -100);
INSERT INTO transacciones_sucias VALUES (7032, '145928-0', 'TELEFONO_X', 'call-center', '2026.10.01', '103', 3, 12000);
INSERT INTO transacciones_sucias VALUES (7033, '187370-0', 'TELEFONO_X', 'APP', '01/10/2026', 'Sin Asignar', 2, -100);
INSERT INTO transacciones_sucias VALUES (7034, '137881-5', 'tel-x', 'Call Center', '2026.10.01', NULL, 3, 12000);
INSERT INTO transacciones_sucias VALUES (7035, '168750-5', 'TELEFONO_X', NULL, '01-10-2026', '103', -100, -100);
INSERT INTO transacciones_sucias VALUES (7036, '130479-5', 'SKU-002', NULL, '2026/10/01', NULL, -100, 30000);
INSERT INTO transacciones_sucias VALUES (7037, '127854-1', 'PROD-A', 'APP', '01/10/2026', NULL, 1, -100);
INSERT INTO transacciones_sucias VALUES (7038, '127854-1', 'TELEFONO_X', 'call-center', '2026-10-01 14:30:00', '101', 3, -50000);
INSERT INTO transacciones_sucias VALUES (7039, '130814-6', 'NOTE-HP', 'app_movil', '01-10-2026', 'N/A', -100, 30000);
INSERT INTO transacciones_sucias VALUES (7040, '187127-8', 'SKU-001', 'app_movil', '2026/10/01', '104', 1, 12000);
INSERT INTO transacciones_sucias VALUES (7041, '145350-3', 'tel-x', 'call-center', '2026-10-01', NULL, 3, -100);
INSERT INTO transacciones_sucias VALUES (7042, '158180-8', 'SKU-001', 'web', '2026/10/01', '103', 1, 12000);
INSERT INTO transacciones_sucias VALUES (7043, '187370-0', 'SKU-003', NULL, '01/10/2026', '102', 2, 12000);
INSERT INTO transacciones_sucias VALUES (7044, '199658-6', 'sku_1', 'Web', '01-10-2026', 'N/A', -5, -100);
INSERT INTO transacciones_sucias VALUES (7045, '127854-1', 'sku_1', 'call-center', '2026.10.01', NULL, -100, 12000);
INSERT INTO transacciones_sucias VALUES (7046, '183296-1', 'PROD-A', 'APP', '01/10/2026', '101', -5, 30000);
INSERT INTO transacciones_sucias VALUES (7047, '187127-8', 'SKU-003', 'Call Center', '01-10-2026', '102', -5, 30000);
INSERT INTO transacciones_sucias VALUES (7048, '127854-1', 'NOTE-HP', NULL, '2026.10.01', NULL, -5, -50000);
INSERT INTO transacciones_sucias VALUES (7049, '130814-6', 'NOTEBOOK-HP', 'Web', '2026-10-01', 'N/A', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7050, '115777-3', 'SKU-001', 'app_movil', '2026/10/01', '104', 1, -50000);
INSERT INTO transacciones_sucias VALUES (7051, '147181-3', 'SKU-003', 'app_movil', '01-10-2026', '101', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7052, '168750-5', 'PROD-A', 'call-center', '2026-10-01', '105', 1, 12000);
INSERT INTO transacciones_sucias VALUES (7053, '127854-1', 'NOTEBOOK-HP', 'Web', '2026-10-01 14:30:00', 'Sin Asignar', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7054, '136786-4', 'SKU-001', 'app_movil', '2026-10-01 14:30:00', NULL, 3, -100);
INSERT INTO transacciones_sucias VALUES (7055, '135833-K', 'SKU-001', 'Tienda_Fisica', '2026-10-01 14:30:00', '104', -100, 30000);
INSERT INTO transacciones_sucias VALUES (7056, '135833-K', 'sku_1', 'app_movil', '01/10/2026', 'N/A', 3, -100);
INSERT INTO transacciones_sucias VALUES (7057, '138559-9', 'PROD-A', 'call-center', '2026-10-01', '105', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7058, '122489-4', 'sku_1', 'Call Center', '2026/10/01', 'N/A', -5, 12000);
INSERT INTO transacciones_sucias VALUES (7059, '187370-0', 'tel-x', 'app_movil', '2026/10/01', '102', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7060, '199658-6', 'NOTEBOOK-HP', NULL, '2026-10-01', 'N/A', 1, -100);
INSERT INTO transacciones_sucias VALUES (7061, '145928-0', 'NOTEBOOK-HP', 'Web', '2026-10-01', '104', -5, -100);
INSERT INTO transacciones_sucias VALUES (7062, '135833-K', 'SKU-001', 'web', '2026-10-01', 'N/A', 2, 12000);
INSERT INTO transacciones_sucias VALUES (7063, '191214-0', 'PROD-A', NULL, '2026-10-01', '105', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7064, '127854-1', 'TELEFONO_X', 'app_movil', '2026-10-01 14:30:00', 'N/A', -5, -50000);
INSERT INTO transacciones_sucias VALUES (7065, '158180-8', 'PROD-A', 'call-center', '2026-10-01 14:30:00', '104', 3, -50000);
INSERT INTO transacciones_sucias VALUES (7066, '168649-1', 'PROD-A', NULL, '2026-10-01 14:30:00', 'N/A', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7067, '187127-8', 'sku_1', 'Web', '2026-10-01', NULL, 3, -100);
INSERT INTO transacciones_sucias VALUES (7068, '199799-K', 'NOTE-HP', 'web', '2026-10-01 14:30:00', '103', 3, 12000);
INSERT INTO transacciones_sucias VALUES (7069, '158180-8', 'tel-x', 'call-center', '01-10-2026', '102', 1, -50000);
INSERT INTO transacciones_sucias VALUES (7070, '137881-5', 'PROD-A', 'call-center', '2026/10/01', '104', 2, -50000);
INSERT INTO transacciones_sucias VALUES (7071, '187370-0', 'NOTE-HP', 'APP', '2026-10-01 14:30:00', NULL, 1, 30000);
INSERT INTO transacciones_sucias VALUES (7072, '122467-5', 'TELEFONO_X', 'web', '01-10-2026', NULL, 1, -100);
INSERT INTO transacciones_sucias VALUES (7073, '191214-0', 'SKU-002', NULL, '2026.10.01', '104', 3, 12000);
INSERT INTO transacciones_sucias VALUES (7074, '158180-8', 'sku_1', 'web', '2026-10-01 14:30:00', 'N/A', 3, -100);
INSERT INTO transacciones_sucias VALUES (7075, '147181-3', 'sku-002', NULL, '2026/10/01', NULL, 2, -50000);
INSERT INTO transacciones_sucias VALUES (7076, '137881-5', 'NOTEBOOK-HP', NULL, '2026-10-01 14:30:00', NULL, -5, 12000);
INSERT INTO transacciones_sucias VALUES (7077, '147181-3', 'PROD-A', 'Call Center', '2026.10.01', '101', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7078, '199658-6', 'PROD-A', 'TIENDA FISICA', '2026-10-01 14:30:00', 'Sin Asignar', 2, 30000);
INSERT INTO transacciones_sucias VALUES (7079, '130479-5', 'sku_1', 'APP', '01-10-2026', NULL, 2, 12000);
INSERT INTO transacciones_sucias VALUES (7080, '147949-K', 'tel-x', NULL, '2026.10.01', '102', -5, 12000);
INSERT INTO transacciones_sucias VALUES (7081, '168649-1', 'SKU-003', 'TIENDA FISICA', '01-10-2026', '106', -5, 30000);
INSERT INTO transacciones_sucias VALUES (7082, '168750-5', 'SKU-003', 'Web', '2026/10/01', '102', -100, 30000);
INSERT INTO transacciones_sucias VALUES (7083, '147949-K', 'TELEFONO_X', NULL, '01/10/2026', '106', -100, -100);
INSERT INTO transacciones_sucias VALUES (7084, '136786-4', 'NOTE-HP', 'APP', '2026-10-01', '103', 3, 12000);
INSERT INTO transacciones_sucias VALUES (7085, '122489-4', 'sku-002', 'APP', '01/10/2026', '102', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7086, '137881-5', 'sku-002', 'call-center', '01/10/2026', 'Sin Asignar', 2, 12000);
INSERT INTO transacciones_sucias VALUES (7087, '138559-9', 'SKU-002', 'app_movil', '01/10/2026', NULL, 2, -50000);
INSERT INTO transacciones_sucias VALUES (7088, '138559-9', 'TELEFONO_X', 'call-center', '2026/10/01', '103', 3, 12000);
INSERT INTO transacciones_sucias VALUES (7089, '121704-6', 'sku_1', 'Web', '2026-10-01 14:30:00', 'N/A', -5, -100);
INSERT INTO transacciones_sucias VALUES (7090, '187127-8', 'PROD-A', 'app_movil', '2026.10.01', '104', 1, 12000);
INSERT INTO transacciones_sucias VALUES (7091, '123194-6', 'NOTE-HP', 'call-center', '01/10/2026', '103', 3, -50000);
INSERT INTO transacciones_sucias VALUES (7092, '127854-1', 'sku-002', NULL, '01/10/2026', 'Sin Asignar', 1, 30000);
INSERT INTO transacciones_sucias VALUES (7093, '145350-3', 'SKU-001', 'APP', '01/10/2026', '106', 3, 30000);
INSERT INTO transacciones_sucias VALUES (7094, '187370-0', 'SKU-001', 'web', '01/10/2026', NULL, 2, 30000);
INSERT INTO transacciones_sucias VALUES (7095, '147181-3', 'sku-002', 'app_movil', '2026/10/01', 'N/A', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7096, '145928-0', 'NOTE-HP', 'APP', '2026/10/01', 'N/A', -5, -100);
INSERT INTO transacciones_sucias VALUES (7097, '147181-3', 'NOTE-HP', 'APP', '2026.10.01', '106', -100, 12000);
INSERT INTO transacciones_sucias VALUES (7098, '196858-8', 'sku-002', 'app_movil', '2026-10-01 14:30:00', NULL, 2, 12000);
INSERT INTO transacciones_sucias VALUES (7099, '137338-8', 'SKU-003', NULL, '01/10/2026', NULL, -100, -50000);
INSERT INTO transacciones_sucias VALUES (7100, '145350-3', 'PROD-A', 'app_movil', '01/10/2026', NULL, 3, 12000);
CREATE TABLE cliente_sucio (
    rut VARCHAR(20),
    nombre_cliente VARCHAR(100),
    email VARCHAR(100),
    segmento VARCHAR(50)
);

INSERT INTO cliente_sucio VALUES ('199658-6', 'Juan Perez', 'juan.p@correo.com', 'VIP');
INSERT INTO cliente_sucio VALUES ('199658-6', 'Juan Perez', 'juan.p@correo.com', 'VIP');
INSERT INTO cliente_sucio VALUES ('145350-3', 'Maria Lopez', NULL, 'Normal');
INSERT INTO cliente_sucio VALUES ('12.246.75-5', 'Carlos', 'carlos@mail', 'N/A');
INSERT INTO cliente_sucio VALUES ('187127-8', NULL, 'anonimo@correo.cl', 'Nuevo');
INSERT INTO cliente_sucio VALUES ('114130-1', 'Ana', 'ana@correo.com', 'VIP');
import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const TraceabilityMatrix = () => {
  const [currentPart, setCurrentPart] = useState(1);

  const allRequirements = [
    { id: 'RF-01', name: 'Gestión de usuarios' },
    { id: 'RF-02', name: 'Creación de proyectos' },
    { id: 'RF-03', name: 'Multiproyecto' },
    { id: 'RF-04', name: 'Seleccionar metodología' },
    { id: 'RF-05', name: 'Asignación de roles' },
    { id: 'RF-06', name: 'Registro de requerimientos' },
    { id: 'RF-07', name: 'Priorización de requerimientos' },
    { id: 'RF-08', name: 'Historial de cambios en requerimientos' },
    { id: 'RF-09', name: 'Agregar archivos a casos de uso' },
    { id: 'RF-10', name: 'Registro de casos de uso' },
    { id: 'RF-11', name: 'Definir dependencias' },
    { id: 'RF-12', name: 'Agrupar requerimientos' },
    { id: 'RF-13', name: 'Adjuntar archivo a requerimiento' },
    { id: 'RF-14', name: 'Adjuntar archivo a caso de uso' },
    { id: 'RF-15', name: 'Generación de matriz de trazabilidad' },
    { id: 'RF-16', name: 'Listar casos de uso sin requerimiento' },
    { id: 'RF-17', name: 'Listar requerimiento sin caso de uso' },
    { id: 'RF-18', name: 'Comentarios en requerimientos' },
    { id: 'RF-19', name: 'Comentarios en casos de uso' },
    { id: 'RF-20', name: 'Notificaciones' },
    { id: 'RF-21', name: 'Generación de informes' },
    { id: 'RF-22', name: 'Visualización gráfica interactiva' }
  ];

  const allCases = ['CU-00', 'CU-01', 'CU-02', 'CU-03', 'CU-04', 'CU-05', 'CU-06', 'CU-07', 'CU-08', 'CU-09', 'CU-10', 'CU-11', 'CU-12', 'CU-13', 'CU-14', 'CU-15', 'CU-16'];

  // Matriz completa de trazabilidad
  const fullMatrix = [
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  ];

  // Configuración de partes: 5 RF x 5 CU cada una
  const parts = [
    { rfStart: 0, rfEnd: 5, cuStart: 0, cuEnd: 5 },    // Parte 1: RF 1-5, CU 0-4
    { rfStart: 0, rfEnd: 5, cuStart: 5, cuEnd: 10 },   // Parte 2: RF 1-5, CU 5-9
    { rfStart: 0, rfEnd: 5, cuStart: 10, cuEnd: 15 },  // Parte 3: RF 1-5, CU 10-14
    { rfStart: 0, rfEnd: 5, cuStart: 15, cuEnd: 17 },  // Parte 4: RF 1-5, CU 15-16
    { rfStart: 5, rfEnd: 10, cuStart: 0, cuEnd: 5 },   // Parte 5: RF 6-10, CU 0-4
    { rfStart: 5, rfEnd: 10, cuStart: 5, cuEnd: 10 },  // Parte 6: RF 6-10, CU 5-9
    { rfStart: 5, rfEnd: 10, cuStart: 10, cuEnd: 15 }, // Parte 7: RF 6-10, CU 10-14
    { rfStart: 5, rfEnd: 10, cuStart: 15, cuEnd: 17 }, // Parte 8: RF 6-10, CU 15-16
    { rfStart: 10, rfEnd: 15, cuStart: 0, cuEnd: 5 },  // Parte 9: RF 11-15, CU 0-4
    { rfStart: 10, rfEnd: 15, cuStart: 5, cuEnd: 10 }, // Parte 10: RF 11-15, CU 5-9
    { rfStart: 10, rfEnd: 15, cuStart: 10, cuEnd: 15 },// Parte 11: RF 11-15, CU 10-14
    { rfStart: 10, rfEnd: 15, cuStart: 15, cuEnd: 17 },// Parte 12: RF 11-15, CU 15-16
    { rfStart: 15, rfEnd: 20, cuStart: 0, cuEnd: 5 },  // Parte 13: RF 16-20, CU 0-4
    { rfStart: 15, rfEnd: 20, cuStart: 5, cuEnd: 10 }, // Parte 14: RF 16-20, CU 5-9
    { rfStart: 15, rfEnd: 20, cuStart: 10, cuEnd: 15 },// Parte 15: RF 16-20, CU 10-14
    { rfStart: 15, rfEnd: 20, cuStart: 15, cuEnd: 17 },// Parte 16: RF 16-20, CU 15-16
    { rfStart: 20, rfEnd: 22, cuStart: 0, cuEnd: 5 },  // Parte 17: RF 21-22, CU 0-4
    { rfStart: 20, rfEnd: 22, cuStart: 5, cuEnd: 10 }, // Parte 18: RF 21-22, CU 5-9
    { rfStart: 20, rfEnd: 22, cuStart: 10, cuEnd: 15 },// Parte 19: RF 21-22, CU 10-14
    { rfStart: 20, rfEnd: 22, cuStart: 15, cuEnd: 17 } // Parte 20: RF 21-22, CU 15-16
  ];

  const totalParts = parts.length;
  const currentConfig = parts[currentPart - 1];
  
  const currentRequirements = allRequirements.slice(currentConfig.rfStart, currentConfig.rfEnd);
  const currentCases = allCases.slice(currentConfig.cuStart, currentConfig.cuEnd);
  
  const currentMatrix = currentRequirements.map((_, rfIndex) => {
    const fullRfIndex = currentConfig.rfStart + rfIndex;
    return currentCases.map((_, cuIndex) => {
      const fullCuIndex = currentConfig.cuStart + cuIndex;
      return fullMatrix[fullRfIndex][fullCuIndex];
    });
  });

  const goToPrevious = () => {
    if (currentPart > 1) setCurrentPart(currentPart - 1);
  };

  const goToNext = () => {
    if (currentPart < totalParts) setCurrentPart(currentPart + 1);
  };

  return (
    <div className="w-full h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6 flex flex-col">
      <div className="bg-white rounded-xl shadow-2xl p-6 flex-1 flex flex-col">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-gray-800">
            Matriz de Trazabilidad
          </h1>
          <div className="flex items-center gap-4">
            <span className="text-sm font-semibold text-gray-600 bg-blue-100 px-4 py-2 rounded-full">
              Parte {currentPart} de {totalParts}
            </span>
            <div className="flex gap-2">
              <button
                onClick={goToPrevious}
                disabled={currentPart === 1}
                className="p-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                title="Anterior"
              >
                <ChevronLeft size={20} />
              </button>
              <button
                onClick={goToNext}
                disabled={currentPart === totalParts}
                className="p-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                title="Siguiente"
              >
                <ChevronRight size={20} />
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-auto">
          <table className="w-full border-collapse">
            <thead className="sticky top-0 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
              <tr>
                <th className="border border-blue-700 p-4 text-left font-semibold text-base min-w-[350px]">
                  Requerimientos / Casos de uso
                </th>
                {currentCases.map((cu) => (
                  <th key={cu} className="border border-blue-700 p-4 font-semibold text-base min-w-[100px]">
                    {cu}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {currentRequirements.map((req, rowIndex) => (
                <tr key={req.id} className={rowIndex % 2 === 0 ? 'bg-blue-50' : 'bg-white'}>
                  <td className="border border-gray-300 p-4">
                    <span className="font-bold text-blue-700 text-base">{req.id}</span>
                    <span className="ml-2 text-gray-700 text-base">{req.name}</span>
                  </td>
                  {currentMatrix[rowIndex].map((value, colIndex) => (
                    <td
                      key={colIndex}
                      className={`border border-gray-300 p-4 text-center ${
                        value === 1 ? 'bg-green-400' : ''
                      }`}
                    >
                      {value === 1 && (
                        <span className="text-white font-bold text-2xl">X</span>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="mt-4 text-center">
          <p className="font-semibold text-gray-700 text-base">
            Requisitos Funcionales vs Casos de Uso - Sistema de Gestión de Requerimientos
          </p>
          <p className="text-sm text-gray-500 mt-1">
            RF {currentConfig.rfStart + 1}-{currentConfig.rfEnd} | CU {currentConfig.cuStart}-{currentConfig.cuEnd - 1}
          </p>
        </div>
      </div>
    </div>
  );
};

export default TraceabilityMatrix;
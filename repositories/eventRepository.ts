import { Event } from '../models/Event'; // Importa o tipo Event da pasta models

export const getAllEvents = async (): Promise<Event[]> => {
  // Esta é uma função de placeholder.
  // Em uma aplicação real, isso buscaria eventos de um banco de dados ou API.
  console.log('getAllEvents chamada - retornando dados mockados');
  return [
    { id: '1', name: 'Evento Passado Público 1', date: new Date('2023-01-15T10:00:00Z'), isPublic: true, description: 'Um evento que já ocorreu.' },
    { id: '2', name: 'Evento Futuro Público 1', date: new Date('2025-08-01T14:30:00Z'), isPublic: true, description: 'Um evento que ainda vai acontecer.' },
    { id: '3', name: 'Evento Futuro Privado', date: new Date('2025-09-10T18:00:00Z'), isPublic: false, description: 'Um evento privado futuro.' },
    { id: '4', name: 'Evento Passado Público 2', date: new Date('2022-11-20T10:00:00Z'), isPublic: true, description: 'Outro evento que já ocorreu.' },
    { id: '5', name: 'Evento Criado em 05/05', date: new Date('2025-05-05T12:00:00Z'), isPublic: true, description: 'Evento criado pelo usuário com data em 05/05/2025.' }, // Data do evento atualizada
  ];
};

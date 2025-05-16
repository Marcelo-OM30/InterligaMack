// Caminho para interligaMack/models/Event.ts
import { Event } from '../../models/Event'; 
// Caminho para interligaMack/models/repositories/eventRepository.ts
import { getAllEvents } from '../../repositories/eventRepository'; 

console.log('eventService.ts: Script loaded');

export const getPublicEvents = async (): Promise<Event[]> => {
  console.log('eventService: Chamando getAllEvents...');
  let allEvents: Event[] = [];
  try {
    allEvents = await getAllEvents();
    console.log('eventService: Eventos recebidos de getAllEvents:', JSON.stringify(allEvents, null, 2));
  } catch (error) {
    console.error('eventService: Erro ao chamar getAllEvents:', error);
    return []; // Retorna array vazio em caso de erro
  }

  // Filtra apenas por eventos públicos, sem a restrição de data que existia antes.
  const publicEvents = allEvents.filter(event => {
    // Log para cada evento antes de filtrar
    // console.log(`eventService: Verificando evento: ${event.name}, isPublic: ${event.isPublic}`);
    return event.isPublic;
  });
  console.log('eventService: Eventos públicos filtrados (após filtro isPublic):', JSON.stringify(publicEvents, null, 2));
  
  return publicEvents;
};

// Para ajudar na depuração, podemos chamar a função quando o script carrega
// e logar o resultado ou tentar exibir em algum lugar se você tiver um elemento para isso.
(async () => {
  try {
    console.log('eventService.ts: Tentando chamar getPublicEvents automaticamente para depuração...');
    const events = await getPublicEvents();
    console.log('eventService.ts: Resultado da chamada automática de getPublicEvents (deve aparecer na página):', JSON.stringify(events, null, 2));
    // Se você tiver um elemento no seu HTML para exibir a saída de depuração, poderia usá-lo aqui.
    // Exemplo:
    // const debugOutputElement = document.getElementById('debug-event-output');
    // if (debugOutputElement) {
    //   debugOutputElement.textContent = JSON.stringify(events, null, 2);
    // }
  } catch (error) {
    console.error('eventService.ts: Erro durante a chamada automática de getPublicEvents:', error);
  }
})();
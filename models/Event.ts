export interface Event {
  id: string; // Ou number, dependendo da sua necessidade
  name: string;
  date: Date; // Importante para a lógica original de filtro de data
  isPublic: boolean; // Usado em eventService.ts
  // Adicione outras propriedades relevantes do evento aqui
  description?: string;
  location?: string;
}

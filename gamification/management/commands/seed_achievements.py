from django.core.management.base import BaseCommand
from gamification.models import RoomItem, Achievement


ITEMS = [
    {'name': 'Cama', 'description': 'Uma cama confortável para sua sala.', 'category': 'furniture', 'asset_key': 'bed', 'position_x': 0.2, 'position_y': 0.6},
    {'name': 'Escrivaninha', 'description': 'Mesa de computador para trabalhar.', 'category': 'furniture', 'asset_key': 'desk', 'position_x': 0.7, 'position_y': 0.6},
    {'name': 'Armário', 'description': 'Armário para organizar suas coisas.', 'category': 'furniture', 'asset_key': 'wardrobe', 'position_x': 0.1, 'position_y': 0.3},
    {'name': 'Planta', 'description': 'Uma plantinha para alegrar o ambiente.', 'category': 'plant', 'asset_key': 'plant', 'position_x': 0.85, 'position_y': 0.8},
    {'name': 'Televisão', 'description': 'TV para relaxar depois de economizar.', 'category': 'electronics', 'asset_key': 'tv', 'position_x': 0.5, 'position_y': 0.3},
    {'name': 'Estante', 'description': 'Estante cheia de livros e conquistas.', 'category': 'furniture', 'asset_key': 'bookshelf', 'position_x': 0.9, 'position_y': 0.4},
    {'name': 'Quadro', 'description': 'Uma obra de arte para decorar a sala.', 'category': 'decoration', 'asset_key': 'painting', 'position_x': 0.5, 'position_y': 0.1},
    {'name': 'Tapete', 'description': 'Tapete que deixa o ambiente mais aconchegante.', 'category': 'decoration', 'asset_key': 'rug', 'position_x': 0.5, 'position_y': 0.7},
]

ACHIEVEMENTS = [
    {
        'name': 'Primeiros Passos',
        'description': 'Registre sua primeira receita.',
        'trigger_type': 'first_income',
        'trigger_value': None,
        'item_key': 'plant',
    },
    {
        'name': 'Primeira Meta Cumprida',
        'description': 'Conclua sua primeira meta de economia.',
        'trigger_type': 'goal_completed',
        'trigger_value': 1,
        'item_key': 'bed',
    },
    {
        'name': 'Liquidador de Dívidas',
        'description': 'Quite sua primeira dívida.',
        'trigger_type': 'debt_paid',
        'trigger_value': 1,
        'item_key': 'desk',
    },
    {
        'name': 'Organizador',
        'description': 'Mantenha 3 meses dentro do orçamento.',
        'trigger_type': 'budget_months',
        'trigger_value': 3,
        'item_key': 'wardrobe',
    },
    {
        'name': 'Poupador',
        'description': 'Acumule R$1.000 em metas concluídas.',
        'trigger_type': 'total_saved',
        'trigger_value': 1000,
        'item_key': 'rug',
    },
    {
        'name': 'Investidor Iniciante',
        'description': 'Acumule R$5.000 em metas concluídas.',
        'trigger_type': 'total_saved',
        'trigger_value': 5000,
        'item_key': 'tv',
    },
    {
        'name': 'Mestre das Metas',
        'description': 'Conclua 5 metas de economia.',
        'trigger_type': 'goal_completed',
        'trigger_value': 5,
        'item_key': 'bookshelf',
    },
    {
        'name': 'Livre de Dívidas',
        'description': 'Quite 3 dívidas diferentes.',
        'trigger_type': 'debt_paid',
        'trigger_value': 3,
        'item_key': 'painting',
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com conquistas e itens de sala iniciais.'

    def handle(self, *args, **kwargs):
        items_map = {}
        for item_data in ITEMS:
            item, created = RoomItem.objects.update_or_create(
                asset_key=item_data['asset_key'],
                defaults=item_data,
            )
            items_map[item.asset_key] = item
            status = 'criado' if created else 'atualizado'
            self.stdout.write(f'  Item {status}: {item.name}')

        for ach_data in ACHIEVEMENTS:
            item_key = ach_data.pop('item_key')
            ach_data['room_item'] = items_map.get(item_key)
            achievement, created = Achievement.objects.update_or_create(
                name=ach_data['name'],
                defaults=ach_data,
            )
            status = 'criada' if created else 'atualizada'
            self.stdout.write(f'  Conquista {status}: {achievement.name}')

        self.stdout.write(self.style.SUCCESS('Seed concluído com sucesso!'))

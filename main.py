import json
import os

def load_library():
    if os.path.exists('bibliotheque.json'):
        with open('bibliotheque.json', 'r') as f:
            library = json.load(f)
        return library
    return []

def save_library(library):
    with open('bibliotheque.json', 'w') as f:
        json.dump(library, f, indent=4)

def generate_id(library):
    if not library:
        return 1
    max_id = max(book['ID'] for book in library)
    return max_id + 1

def display_books(library):
    if not library:
        print("Aucun livre trouvé.")
        return
    for book in library:
        statut = 'oui' if book['Lu'] else 'non'
        print(f"ID: {book['ID']}")
        print(f"Titre: {book['Titre']}")
        print(f"Auteur: {book['Auteur']}")
        print(f"Année: {book['Année']}")
        print(f"Lu: {statut}")
        if book['Note'] is not None:
            print(f"Note: {book['Note']} /10")
            print(f"Commentaire: {book['Commentaire']}")
        print('-----------------------')

def add_book(library):
    title = input('Titre du livre : ')
    author = input('Auteur du livre : ')
    year = input('Année de publication : ')
    try:
        year = int(year)
    except ValueError:
        print('Année invalide. Le livre n\'a pas été ajouté.')
        return
    new_book = {
        'ID': generate_id(library),
        'Titre': title,
        'Auteur': author,
        'Année': year,
        'Lu': False,
        'Note': None,
        'Commentaire': ''
    }
    library.append(new_book)
    print('Livre ajouté.')

def delete_book(library):
    id_str = input('ID du livre à supprimer : ')
    try:
        id_deleted = int(id_str)
    except ValueError:
        print('ID invalide.')
        return
    for book in library:
        if book['ID'] == id_deleted:
            library.remove(book)
            print('Livre supprimé.')
            return
    print('Livre non trouvé.')

def search_book(library):
    w = input('Mot-clé (titre ou auteur) : ').lower()
    r = []
    for book in library:
        if w in book['Titre'].lower() or w in book['Auteur'].lower():
            r.append(book)
    if len(r) > 0:
        display_books(r)
    else:
        print('Aucun résultat.')

def mark_read(library):
    id_str = input('ID du livre lu : ')
    try:
        id_lu = int(id_str)
    except ValueError:
        print('ID invalide.')
        return
    for book in library:
        if book['ID'] == id_lu:
            book['Lu'] = True
            score = input('Note sur 10 : ')
            try:
                score = int(score)
                if score < 0 or score > 10:
                    raise ValueError
                book['Note'] = score
            except ValueError:
                print("Note invalide, elle doit être entre 0 et 10.")
                book['Note'] = None
            book['Commentaire'] = input('Commentaire : ')
            print('Livre mis à jour.')
            return
    print('Livre non trouvé.')

def filter_books(library, lu=True):
    filtres = [book for book in library if book['Lu'] == lu]
    display_books(filtres)

def sort_books(library):
    choice = input('Trier par (1) année, (2) auteur, (3) note : ')
    if choice == '1':
        sorted_books = sorted(library, key=lambda x: x['Année'])
    elif choice == '2':
        sorted_books = sorted(library, key=lambda x: x['Auteur'].lower())
    elif choice == '3':
        sorted_books = sorted(library, key=lambda x: (x['Note'] or 0), reverse=True)
    else:
        print("Choix invalide.")
        return
    display_books(sorted_books)

def menu():
    library = load_library()
    while True:
        print('\n=== MENU ===')
        print('1. Voir tous les livres')
        print('2. Ajouter un livre')
        print('3. Supprimer un livre')
        print('4. Rechercher un livre')
        print('5. Marquer un livre comme lu')
        print('6. Livres déjà lus')
        print('7. Livres à lire')
        print('8. Trier les livres')
        print('9. Quitter')
        choice = input('Votre choix : ')
        if choice == '1':
            display_books(library)
        elif choice == '2':
            add_book(library)
        elif choice == '3':
            delete_book(library)
        elif choice == '4':
            search_book(library)
        elif choice == '5':
            mark_read(library)
        elif choice == '6':
            filter_books(library, True)
        elif choice == '7':
            filter_books(library, False)
        elif choice == '8':
            sort_books(library)
        elif choice == '9':
            save_library(library)
            print('Données sauvegardées. À bientôt !')
            break
        else:
            print('Choix invalide.')


if __name__ == '__main__':
    menu()
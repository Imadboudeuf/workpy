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
    if len(library) == 0:
        return 1
    big_id = library[0]['ID']
    for book in library:
        if book['ID'] > big_id:
            big_id = book['ID']
    return big_id + 1

def display_books(library):
    for book in library:
        statut = 'oui' if book['Lu'] else 'non'
        print('ID:', book['ID'])
        print('Titre:', book['Titre'])
        print('Auteur:', book['Auteur'])
        print('Année:', book['Année'])
        print('Lu:', statut)
        if book['Note'] is not None:
            print('Note:', book['Note'], '/10')
            print('Commentaire:', book['Commentaire'])
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
    f = False
    for book in library:
        if book['ID'] == id_deleted:
            library.remove(book)
            print('Livre supprimé.')
            f = True
            break
    if not f:
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
    f = False
    for book in library:
        if book['ID'] == id_lu:
            book['Lu'] = True
            score = input('Note sur 10 : ')
            try:
                book['Note'] = int(score)
            except ValueError:
                book['Note'] = None
            book['Commentaire'] = input('Commentaire : ')
            print('Livre mis à jour.')
            f = True
            break
    if not f:
        print('Livre non trouvé.')

def filter_books(library, lu=True):
    filtres = []
    for book in library:
        if book['Lu'] == lu:
            filtres.append(book)
    display_books(filtres)

def sort_books(library):
    choice = input('Trier par (1) année, (2) auteur, (3) note : ')
    if choice == '1':
        for i in range(len(library)):
            for j in range(i + 1, len(library)):
                if library[i]['Année'] > library[j]['Année']:
                    library[i], library[j] = library[j], library[i]
    elif choice == '2':
        for i in range(len(library)):
            for j in range(i + 1, len(library)):
                if library[i]['Auteur'] > library[j]['Auteur']:
                    library[i], library[j] = library[j], library[i]
    elif choice == '3':
        for i in range(len(library)):
            for j in range(i + 1, len(library)):
                note_i = library[i]['Note'] or 0
                note_j = library[j]['Note'] or 0
                if note_i < note_j:
                    library[i], library[j] = library[j], library[i]
    display_books(library)

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

from .Company import Company


def main(q, selfurl):
    print("Content-type: text/html; charset=utf-8\n\n")
    company = Company(q, selfurl)
    ACTIONS = {
        'display': company.display_staff,
        'add_employee': company.add_employee,
        'add_supervisor': company.add_supervisor,
        'save_employee': company.save_employee,
        'save_supervisor': company.save_supervisor,
        'clear_list': company.clear_staff,
        'delete_person': company.remove_person,
        'edit_employee': company.edit_person,
        'edit_supervisor': company.edit_person,
        'import': company.read_from_file
    }
    if 'action' in q:
        ACTIONS[q['action'].value]()
    else:
        ACTIONS['display']()


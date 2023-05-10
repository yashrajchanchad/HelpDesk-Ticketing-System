TICKET_STATUS = (
    ('open', 'open'),
    ('closed', 'closed'),
    ('working', 'working'),
    ('hold','hold'),
    ('resolve','resolve'),
)
USER_TICKET_STATUS = (
    ('open', 'open'),
    ('closed', 'closed'),
)

MANAGER_TICKET_STATUS = (
    ('open', 'open'),
    ('closed', 'closed'),
    ('working', 'working'),
    ('hold','hold'),
    ('resolve','resolve'),
)
ENGINEER_TICKET_STATUS = (
    ('open', 'open'),
    ('working', 'working'),
    ('hold','hold'),
    ('resolve','resolve'),
)

PRIORITY = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Critical', 'Critical'),
)

DEPARTMENT = (
    ('HR', 'HR'),
    ('Admin', 'Admin'),
    ('Tech', 'Tech'),
    ('Devops', 'Devops'),
    ('AI', 'AI')
)
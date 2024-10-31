from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
sequence_to_classify = "Принципы объектно-ориентированного программирования; Основные структуры данных и алгоритмы; Знание Java Core; Уверенная работа с Git; Внедрение и поддержка CI/CD; Spring и Hibernate frameworks; Опыт работы с kubernetes, docker swarm; СУБД SQL Server, PostgreSQL, Oracle; Умение работать с одним из брокеров очередей (Active MQ/Rabbit MQ/IBM MQ/Kafka); Навыки работы с REST API, SOAP; Практический опыт работы с HTML, CSS, React, JavaScript; Опыт работы с фронтенд-фреймворками, такими как Angular, Vue; Умение разбираться в чужом исходном коде; Понимание принципов обеспечения безопасности приложений; Понимание архитектуры приложений; PL/SQL; Хорошее знание модулей Oracle E-Business Suite: Supplier Lifecycle Management, Sourcing, iSupplier, Purchasing, Inventory, Product Hub, Procurement Contracts; Опыт с открытыми интерфейсами EBS Open Interfaces и API; конвертации данных, интеграции данных; Опыт с инструментами разработки Oracle: SQL Developer, SQL, PL/SQL, Java EE; Не менее 5-ти лет опыта разработки в области Oracle e-Business Suite. Адаптивность; Ответственность; Сотрудничество и взаимодействие; Гибкость мышления; Умение работать в команде; Целеустремленность; Творчество и креативность; Стрессоустойчивость; Самостоятельность и ответственность; Письменные коммуникативные навыки; Клиентоориентированность."
candidate_labels = ['object-oriented programming', 'data structures and algorithms', 'software engineering', 'web development', 'mobile app development', 'database management', 'distributed systems', 'network programming', 'software testing', 'design patterns', 'Java frameworks', 'cloud computing', 'machine learning', 'devops', 'cybersecurity','networking', 'web development', 'cybersecurity', 'cloud computing', 'data analytics', 'artificial intelligence', 'human-computer interaction', 'project management', 'systems analysis', 'mobile app development', 'machine learning']

result = classifier(sequence_to_classify, candidate_labels, multi_label=True)

# print(result)
# Original result scores and labels
labels = result['labels']
scores = result['scores']

# Define custom weights for specific skills
weights = {'database management': 1.2, 'networking': 1.1}  # Increase scores by 20% and 10% respectively

# Apply weights to the scores
adjusted_scores = [score * weights.get(label, 1) for label, score in zip(labels, scores)]

# Combine labels with adjusted scores and sort by new scores
adjusted_results = sorted(zip(labels, adjusted_scores), key=lambda x: x[1], reverse=True)

# Print the adjusted results
for label, score in adjusted_results:
    print(f'{label}: {score:.4f}')
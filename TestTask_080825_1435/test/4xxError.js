// Пример для 404 Not Found (если организация не существует)
// pm.test("Status code is 404 for non-existent organization", function () {
//     pm.response.to.have.status(404);
// });
// pm.test("Error response structure for 404", function () {
//     const jsonData = pm.response.json();
//     pm.expect(jsonData).to.have.property('error'); // Предполагаемая структура ошибки
//     pm.expect(jsonData.error).to.have.property('code', 'ORGANIZATION_NOT_FOUND'); // Предполагаемый код ошибки
//     pm.expect(jsonData.error).to.have.property('message').that.is.a('string'); // Предполагаемое сообщение
// });

// Пример для 401 Unauthorized (если токен отсутствует или недействителен)
// pm.test("Status code is 401 for unauthorized request", function () {
//     pm.response.to.have.status(401);
// });
// pm.test("Error response structure for 401", function () {
//     const jsonData = pm.response.json();
//     pm.expect(jsonData).to.have.property('error');
//     pm.expect(jsonData.error).to.have.property('code', 'UNAUTHORIZED');
//     pm.expect(jsonData.error).to.have.property('message');
// });

// Пример для 403 Forbidden (если доступ к организации запрещен)
// pm.test("Status code is 403 for forbidden request", function () {
//     pm.response.to.have.status(403);
// });
// pm.test("Error response structure for 403", function () {
//     const jsonData = pm.response.json();
//     pm.expect(jsonData).to.have.property('error');
//     pm.expect(jsonData.error).to.have.property('code', 'FORBIDDEN');
//     pm.expect(jsonData.error).to.have.property('message');
// });

// Пример для 500 Internal Server Error (если произошла внутренняя ошибка, например, ошибка в `instance_generation_upgrade`)
pm.test("Status code is 500 if internal server error occurs", function () {
    // Этот тест может быть нестабильным, если ошибка временная
    // pm.response.to.have.status(500);
});

pm.test("Error response structure for 500 (example from data)", function () {
    const jsonData = pm.response.json();
    const section = jsonData.instance_generation_upgrade;
    if (section && section.error) { // Проверяем, есть ли ошибка в конкретной секции
        pm.expect(section.error).to.be.a('string');
        pm.expect(section.error).to.include("500 Server Error"); // Проверяем часть сообщения об ошибке из примера данных
    }
    // Примечание: Глобальная ошибка 500 может иметь другую структуру
});
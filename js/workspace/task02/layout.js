const todosLayout = (() => {
    const showTodos = (todos) => {
        const tbody = document.querySelector("tbody");

        todos = todos.slice(0, 20);

        let text = ``;
        todos.forEach((todo) => {
            text += `
                <tr>
                    <td>${todo.userId}</td>
                    <td class = "status-${todo.completed}">${todo.title}</td>
                </tr>
            `;
        });

        tbody.innerHTML = text;
    };

    return { showTodos: showTodos };
})();

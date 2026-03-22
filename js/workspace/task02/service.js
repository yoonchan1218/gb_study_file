const todoService = (() => {
    const getList = async (callback) => {
        const response = await fetch(
            "https://jsonplaceholder.typicode.com/todos"
        );
        const todos = await response.json();

        if (callback) {
            callback(todos);
        }
    };

    return { getList: getList };
})();

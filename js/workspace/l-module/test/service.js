const userService = (() => {
    const getUserById = async (userId, callback) => {
        try {
            const response = await fetch(
                `https://jsonplaceholder.typicode.com/users/${userId}`
            );
            const user = await response.json();

            if (callback) {
                callback(user);
            }
        } catch (err) {
            console.log(err);
        }
    };

    return { getUserById: getUserById };
})();

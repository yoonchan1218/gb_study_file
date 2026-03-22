const postService = (() => {
    const getList = async (page, callback) => {
        const response = await fetch(
            "https://jsonplaceholder.typicode.com/posts"
        );
        const posts = await response.json();

        if (callback) {
            callback(page, posts);
        }
    };

    return { getList: getList };
})();

// fetch("https://jsonplaceholder.typicode.com/posts")
//         .then((response) => response.json())
//         .then((posts) => {
//             result = posts;
//         });
// const getPosts = async () => {
//     try {
//         const response = await fetch(
//             "https://jsonplaceholder.typicode.com/posts"
//         );
//         const posts = await response.json();
//         posts.forEach((post, i) => {
//             console.log(i + 1, post.title);
//         });
//     } catch (err) {
//         console.log(err);
//     }
// };

// getPosts();

const postService = (() => {
    const getList = async (callback, page = 1) => {
        try {
            const response = await fetch(
                "https://jsonplaceholder.typicode.com/posts"
            );
            const posts = await response.json();

            if (callback) {
                callback(posts);
            }
        } catch (err) {
            console.log(err);
        }
    };

    return { getList: getList };
})();

const printPostTitles = (posts) => {
    posts
        .map((post) => post.title)
        .forEach((title) => {
            console.log(title);
        });
};

postService.getList(printPostTitles);

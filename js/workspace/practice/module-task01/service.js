const commentService = (() => {
    const getCommentList = async (postId, callback) => {
        try {
            const response = await fetch(
                `https://jsonplaceholder.typicode.com/comments?postId=${postId}`
            );
            const comments = await response.json();
            if (callback) {
                callback(postId, comments);
            }
        } catch (err) {
            console.log(err);
        }
    };
    return { getCommentList: getCommentList };
})();

const commentsLayout = (() => {
    const showComments = (comments) => {
        const tbody = document.querySelector("table tbody");
        let text = ``;
        comments.forEach((comment) => {
            text += ` <tr>
                <th>${comment.name}</th>
                <th>${comment.emil}</th>
                <th>${comment.body}</th>
            </tr>`;
        });
        tbody.innerHTML = text;
    };
    return { showComments: showComments };
})();

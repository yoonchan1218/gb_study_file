const postLayout = (() => {
    const showList = async (page, posts) => {
        const tbody = document.querySelector("table.posts tbody");
        let text = ``;

        let pageSize = 10;
        let start = (page - 1) * pageSize;
        let end = page * pageSize;

        posts = posts.slice(start, end);
        posts.forEach((post) => {
            text += `
                <tr>
                    <td>${post.id}</td>
                    <td>${post.userId}</td>
                    <td>${post.title}</td>
                    <td>${post.body}</td>
                </tr>            
            `;
        });

        tbody.innerHTML = text;
    };

    return { showList: showList };
})();

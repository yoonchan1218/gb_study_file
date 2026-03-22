const userLayout = (() => {
    const showUser = (user) => {
        const tbody = document.querySelector("table tbody");

        tbody.innerHTML = `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>
            </tr>
        `;
    };

    return { showUser: showUser };
})();

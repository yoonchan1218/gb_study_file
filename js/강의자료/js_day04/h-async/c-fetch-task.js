// 서버에서 게시글 목록 요청하기
// 받은 게시글 중 id가 짝수인 게시글의 아이디와 제목 출력하기
// const getList = async () => {
//     const response = await fetch("https://jsonplaceholder.typicode.com/posts");
//     const posts = await response.json();

//     posts
//         .filter((post) => post.id % 2 === 0)
//         .forEach(({ id, title }) => {
//             console.log(id, title);
//         });
// };

// getList();

// 전달받은 댓글들 중, postId가 3인 댓글 내용 출력
// const getRepliesByPostId = async (postId) => {
//     const response = await fetch(
//         "https://jsonplaceholder.typicode.com/comments"
//     );
//     const replies = await response.json();
//     replies
//         .filter((reply) => (reply.postId = postId))
//         .forEach(({ postId, body }) => {
//             console.log(postId, body);
//         });
// };

// getRepliesByPostId(3);

// 전달받은 회원들 중, zipcode만 출력
// const getUserZipcode = async () => {
//     const response = await fetch("https://jsonplaceholder.typicode.com/users");
//     const users = await response.json();

//     console.log(users.map((user) => user.address.zipcode));
// };

// getUserZipcode();

// 게시글 정보를 전달받은 후,
// 게시글 조회를 모듈화하여 사용한다.
// 게시글 조회시, 회원의 번호를 전달받아서 그 작성자의 게시글만 가져온다.
// 전체 정보를 출력한다.
// const postService = (() => {
//     const getList = async (userId, callback) => {
//         const response = await fetch(
//             "https://jsonplaceholder.typicode.com/posts"
//         );
//         const posts = await response.json();
//         if (callback) {
//             callback(posts, userId);
//         }
//     };

//     return { getList: getList };
// })();

// const postLayout = (() => {
//     const showPostsByUserId = (posts, userId) => {
//         console.log(posts.filter((post) => post.userId === userId));
//     };

//     return { showPostsByUserId: showPostsByUserId };
// })();

// const printPostsByUserId = () => {
//     postService.getList(4, postLayout.showPostsByUserId);
// };

// printPostsByUserId();

// 앨범 정보를 전달받은 후,
// 회원 번호가 5인 정보를 모두 가져온다.
// 그 중 userId와 title만 출력한다.
const albumService = (() => {
    const getList = async (userId, callback) => {
        try {
            const response = await fetch(
                "https://jsonplaceholder.typicode.com/albums"
            );
            const albums = await response.json();
            if (callback) {
                callback(userId, albums);
            }
        } catch (err) {
            console.log(err);
        }
    };
    return { getList: getList };
})();

const albumLayout = (() => {
    const showAlbumsByUserId = (userId, albums) => {
        console.log(
            albums
                .filter((album) => album.userId === userId)
                .map(({ userId, title }) => ({ userId, title }))
        );
    };

    return { showAlbumsByUserId: showAlbumsByUserId };
})();

const printAlbumsByUserId = () => {
    albumService.getList(5, albumLayout.showAlbumsByUserId);
};

printAlbumsByUserId();

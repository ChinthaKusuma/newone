document.addEventListener("DOMContentLoaded", function () {
  // Like/Dislike functionality
  const likeCounter = document.getElementById("like-count");
  const likeButton = document.getElementById("like-button");
  const disLikeButton = document.getElementById("dislike-button");

  function addLike() {
    likeButton.classList.toggle("active");
    fetch(`/videos/like/${videoId}/`)
      .then((response) => response.json())
      .then((data) => {
        likeButton.innerHTML = data;
        loadLikes();
      })
      .catch((error) => console.error("Error:", error));
  }

  function loadLikes() {
    fetch(`/videos/likes/${videoId}/`)
      .then((response) => response.json())
      .then((data) => {
        likeCounter.innerText = data.length;
      })
      .catch((error) => console.error("Error:", error));
  }

  function disLike() {
    disLikeButton.classList.toggle("active1");
  }

  likeButton.addEventListener("click", addLike);
  disLikeButton.addEventListener("click", disLike);
  loadLikes();

  // Comments functionality
  const commentForm = document.getElementById("comment-form");

  if (commentForm) {
    commentForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const form = e.target;
      const formData = new FormData(form);
      const videoId = form.getAttribute("data-video-id");

      fetch(`/comment/add/${videoId}/`, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
      })
        .then((response) => response.text())
        .then((data) => {
          document
            .getElementById("comment-section")
            .insertAdjacentHTML("afterbegin", data);
          form.reset();
        })
        .catch((error) => console.error("Error:", error));
    });
  }

  // Reply functionality
  document.querySelectorAll(".reply-form").forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const replyForm = e.target;
      const formData = new FormData(replyForm);
      const commentId = replyForm.getAttribute("data-comment-id");

      fetch(`/comment/reply/${commentId}/`, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
        .then((response) => response.text())
        .then((data) => {
          replyForm.parentElement
            .querySelector(".replies")
            .insertAdjacentHTML("beforeend", data);
          replyForm.style.display = "none";
          replyForm.reset();
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  // Toggle reply forms
  document.querySelectorAll(".reply-toggle").forEach((button) => {
    button.addEventListener("click", function () {
      const commentId = button.getAttribute("data-comment-id");
      const replyForm = document.querySelector(
        `.reply-form[data-comment-id='${commentId}']`
      );
      replyForm.style.display =
        replyForm.style.display === "none" ? "block" : "none";
    });
  });
});

function confirmNewUser(e) {
  const $urlInput = $('#confirmUserURL'),
    url = $urlInput.val(),
    $token = $('input[name="csrfmiddlewaretoken"]');

  $.post(
    url,
    {
      csrfmiddlewaretoken: $token.val()
    }
  );
}

function showNewUserModal($) {
  const $hfShowModal = $('#showNewUserModal'),
    $newUserModal = $('#newUserModal'),
    $newUserModalBtn = $('#newUserModalBtn'),
    showModal = $hfShowModal ? $hfShowModal.val() : false;

  if (showModal === 'True') {
    $newUserModal.modal();
  }

  $newUserModalBtn.click(confirmNewUser);
}

if (jQuery !== 'undefined') {
  jQuery(document).ready(($) => {
    showNewUserModal($);
  });
}

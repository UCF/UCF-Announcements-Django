function confirmNewUser() {
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
    $newUserModelClose = $('#newUserModelClose'),
    showModal = $hfShowModal ? $hfShowModal.val() : false;

  if (showModal === 'True') {
    $newUserModal.modal();
  }

  $newUserModalBtn.click(confirmNewUser);
  $newUserModelClose.click(confirmNewUser);
}

if (jQuery !== 'undefined') {
  jQuery(document).ready(($) => {
    showNewUserModal($);
  });
}

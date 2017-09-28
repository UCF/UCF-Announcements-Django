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
    showModal = $hfShowModal ? $hfShowModal.val() : false;

  if (showModal === 'True') {
    $newUserModal.modal();
  }

  $newUserModal.on('hide.bs.modal', confirmNewUser);
}

function initDatepickers($) {
  const testDate = document.createElement('input');
  testDate.type = 'date';

  if (testDate.type === 'text') {
    $('.date-picker').datepicker({
      dateFormat: 'yy-mm-dd'
    });
  }
}

if (jQuery !== 'undefined') {
  jQuery(document).ready(($) => {
    showNewUserModal($);
    initDatepickers($);
  });
}

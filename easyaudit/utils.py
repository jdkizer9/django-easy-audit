def get_client_ip(meta):
    """Returns the IP of the request, accounting for the possibility of being
    behind a proxy.
    """
    ip = meta.get("HTTP_X_FORWARDED_FOR", None)
    if ip:
        # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
        ip = ip.split(", ")[0]
    else:
        ip = meta.get("REMOTE_ADDR", "")
    return ip

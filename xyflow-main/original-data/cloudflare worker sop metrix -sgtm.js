export default {
  async fetch(request, env, ctx) {
    let { pathname, search, host } = new URL(request.url);
   
    // Remove /metrics/ prefix and replace with root path
    pathname = pathname.replace('/metrics/', '/');
   
    // Your sGTM domain
    const domain = 'sgtm.messerattach.com';
   
    // Create new request
    let newRequest = new Request((`https://` + domain + pathname + search), request);
    newRequest.headers.set('Host', domain);
   
    return fetch(newRequest);
  },
};
export class MessagesResponse {
    constructor() {
        this.data = [];
    }
}

export const useGetMessages = () => {
    return {
        messages: new MessagesResponse()
    };
};

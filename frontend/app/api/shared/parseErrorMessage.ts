export default async function parseErrorMessage(res: Response, defaultPhrase: string = "Непредвиденная ошибка. Обратитесь к администратору"): Promise<string> {
    const errorData = await res.json().catch(() => ({}));
    console.error(errorData);
    if (typeof errorData.detail == "object") {
        return defaultPhrase;
    }
    return errorData.detail || defaultPhrase;
}
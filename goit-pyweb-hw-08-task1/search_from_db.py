from models import Author, Quote
import connect
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def search_name_results(value):
    print(f"Without cache: name={value}")
    return Quote.objects(author__in=Author.objects.filter(fullname__iregex=value))

@cache
def search_tag_results(value):
    print(f"Without cache: name={value}")
    return Quote.objects.filter(tags__iregex=value)

@cache
def search_tags_results(value):
    print(f"Without cache: name={value}")
    return Quote.objects.filter(tags__iregex="|".join(value.split(",")))

def main():
    while True:
        search_info=input("Input search parameters ")

        if any(x in search_info for x in ["name:", "tag:", "tags:"]):
            command, value = search_info.split(":")
            command = command.strip()
            value = value.strip()
            results_list = []

            match command:
                case "name":
                    results_list = search_name_results(value)
                case "tag":
                    results_list = search_tag_results(value)
                case "tags":
                    results_list = search_tags_results(value)

            if not results_list:
                print("results not found")
            else:
                [print(result.quote.encode("utf-8").decode("utf-8")) for result in results_list]
        elif "exit" in search_info:
            break
        else:
            print("Bad command")

if __name__ == '__main__':
    main()

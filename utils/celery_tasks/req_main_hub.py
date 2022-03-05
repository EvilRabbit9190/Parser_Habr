import aiohttp, asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from asgiref.sync import sync_to_async

from getHubs.models import Hubs


class RequestHub:
    def __init__(self) -> None:
        """
            Initialization
        """
        self.hub_links = []
        self.ua = UserAgent()
        self.site = "https://habr.com"
        self.header_accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

    @sync_to_async
    def add_database(self, header: str, date: str, link_post: str, author_name: str, author_link: str, post_id: str, content: str) -> None:
        """
            Add information hub to database
        """
        try:
            # Checking for the existence of a post
            post_exist = self.check_exist_post(post_id)
            if not post_exist:
                post = Hubs.objects.create(
                    header=header,
                    date=date,
                    link_post=link_post,
                    author_name=author_name,
                    author_link=author_link,
                    post_id=post_id,
                    content=content
                )
            else:
                print(" ================ This post has already been added to the database ================ ")
        except Exception as exc:
            print("Exception add database: ", exc)
    
    def check_exist_post(self, post_id) -> bool:
        """
            Check Exist post in the database
        """
        return Hubs.objects.filter(post_id=post_id).exists()

    async def get_text_link(self, session, link: str, data_post: dict) -> None:
        try:
            # Request
            headers = {
                "accept": self.header_accept,
                "User-Agent": self.ua.random
            }
            async with session.get(url=link, headers=headers) as response:
                try:
                    # Parsing all links article
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    block_content = soup.find("article", {"class": "tm-article-presenter__content"})
                    post_content = block_content.find("div", {"id": "post-content-body"})
                    sub_post_content = post_content.find("div", {"class": "article-formatted-body"}).find("div").getText()

                    # Add to database
                    await self.add_database(
                        header=data_post['Header'], 
                        date=data_post['Date'], 
                        link_post=data_post['Link_post'], 
                        author_name=data_post['Author_name'], 
                        author_link=data_post['Author_link'], 
                        post_id=data_post['Post_id'],
                        content=sub_post_content
                    )
                except Exception as exc:
                    print("Exception parser content: ", exc)
            print('======'*30)
        except Exception as exc:
            print("Exception get hub links: ", exc)

    async def run(self):
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "accept": self.header_accept,
                    "User-Agent": self.ua.random
                }
                url_hub = f"{self.site}/ru/hub/infosecurity/"
                response = await session.get(url=url_hub, headers=headers)
                # Parsing all links article
                soup = BeautifulSoup(await response.text(), "html.parser")
                block_articles = soup.find("div", {"class": "tm-articles-list"})
                links_articles = block_articles.find_all("div", {"class": "tm-article-snippet"})
                links_megapost = block_articles.find_all("div", {"class": "tm-megapost-snippet"})

                if not links_megapost:
                    pass
                else:
                    for link_megapost in links_megapost:
                        try:
                            # Link to post
                            link_title = link_megapost.find("a", {"class": "tm-megapost-snippet__card"})
                            link_post = f"{self.site}{link_title.get('href')}"
                            # Post id
                            post_id = link_title.get('href').split("/")[-2]
                            
                            # Header
                            header_post = link_title.find("h2").text
                            
                            # Block Author
                            block_author = link_megapost.find("header", {"class": "tm-megapost-snippet__header"})
                            
                            # Author name
                            author_name = block_author.find("a", {"class": "tm-megapost-snippet__company-blog"})
                            if author_name:
                                author_name = author_name.find("span").text
                            else:
                                author_name = "Habr"
                            
                            # Link to the author
                            author_link = block_author.find("a", {"class": "tm-megapost-snippet__company-blog"})
                            if author_link:
                                author_link = author_link.get('href')
                            else:
                                author_link = "https://habr.com/ru"
                            
                            # Date pablished
                            date = block_author.find("a", {"class": "tm-megapost-snippet__date"}) \
                                            .find("time")["title"] \
                                            .split(",")[0]
                            
                            # Data console output
                            print("Header: ", header_post)
                            print("Date: ", date)
                            print("Link_post: ", link_post)
                            print("post_id: ", post_id)
                            print("Author_name: ", author_name)
                            print("Author_link: ", author_link)

                            # Adding Collected Data to a Variable
                            self.hub_links.append(
                                {"Header": header_post, "Date": date, "Link_post": link_post, "Post_id": post_id, "Author_name": author_name, "Author_link": author_link}
                            )
                            
                            print('==========='*10)
                        except Exception as exc:
                            print("Exception megapost snippet: ", exc)
                    
                if not links_articles:
                    pass
                else:
                    for link_article in links_articles:
                        try:
                            # Link to post
                            link_title = link_article.find("a", {"class": "tm-article-snippet__title-link"})
                            link_post = f"{self.site}{link_title.get('href')}"
                            
                            # Post id
                            post_id = int(link_title.get('href').split("/")[-2])
                            
                            # Header
                            header_post = link_title.find("span").text
                            
                            # Block Author
                            block_author = link_article.find("span", {"class": "tm-article-snippet__author"}) \
                                                        .find("a", {"class": "tm-user-info__userpic"})
                            # Author name
                            author_name = block_author["title"]
                            
                            # Link to the author
                            author_link = f"{self.site}{block_author.get('href')}"
                            
                            # Date pablished
                            date = link_article.find("span", {"class": "tm-article-snippet__datetime-published"}) \
                                                    .find("time")["title"] \
                                                    .split(",")[0]

                            # Data console output
                            print("Header: ", header_post)
                            print("Date: ", date)
                            print("Link_post: ", link_post)
                            print("Post ID: ", post_id)
                            print("Author_name: ", author_name)
                            print("Author_link: ", author_link)

                            # Adding Collected Data to a Variable
                            self.hub_links.append(
                                {"Header": header_post, "Date": date, "Link_post": link_post, "Post_id": post_id, "Author_name": author_name, "Author_link": author_link}
                            )

                            print('==========='*10)
                        except Exception as exc:
                            print("Exception article snippet: ", exc)
            
                # Creating a task
                tasks = []
                for link in self.hub_links:
                    task = asyncio.create_task(self.get_text_link(session, link['Link_post'], link))
                    tasks.append(task)
                
                await asyncio.gather(*tasks)
        except Exception as exc:
            print("Exception gather data: ", exc)
